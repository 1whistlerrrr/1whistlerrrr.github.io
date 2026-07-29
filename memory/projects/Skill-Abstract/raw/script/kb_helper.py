#!/usr/bin/env python3
"""
知识库助手：从 AI 会话中提取知识，写入结构化卡片到 memory 目录。

用法：
  python3 kb_helper.py list [--limit N]          # 列出最近 N 个会话（JSON）
  python3 kb_helper.py qa <index>                 # 提取第 N 个会话的 Q&A（JSON）
  python3 kb_helper.py write-card '<json>'        # 写入一张知识卡片
  python3 kb_helper.py update-index               # 更新 MEMORY.md 索引

write-card 的 JSON 参数格式：
  {
    "name": "知识点标题",
    "description": "一句话描述",
    "dimensions": ["agent", "RAG"],
    "tags": ["chunking", "retrieval"],
    "source_session": "session-file-name.jsonl",
    "source_turn": 3,
    "body": "## 要点\\n\\n核心内容...\\n\\n## 关联\\n- [[other-card]]"
  }
"""
import json
import os
import sys
import argparse
from datetime import datetime

# ── 复用 extract_qa 的能力 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from extract_qa import (
    scan_all_sessions,
    extract_qa,
    get_cached_meta,
)

# ── 记忆库目录 ──
MEMORY_DIR = os.path.expanduser(
    "~/.claude/projects/-Users-liuchuyao-Library-Mobile-Documents-com-apple-CloudDocs-Documents-Code-mini-mind/memory"
)


def format_duration(start_ts, end_ts):
    """两个时间戳 → 人类可读时长"""
    if start_ts is None or end_ts is None:
        return "?"
    secs = int(end_ts - start_ts)
    if secs < 0:
        secs = 0
    if secs < 60:
        return f"{secs}s"
    if secs < 3600:
        return f"{secs // 60}m"
    h = secs // 3600
    m = (secs % 3600) // 60
    return f"{h}h{m:02d}m" if m else f"{h}h"


def format_ts(ts):
    """Unix timestamp → 可读时间字符串"""
    if ts is None:
        return "?"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def list_sessions(limit=15):
    """
    返回最近 N 个会话的列表（JSON 数组）。
    每个元素包含 index（1-based）、标题、时间、时长、轮次数、工具来源。
    """
    sessions = scan_all_sessions()
    if not sessions:
        print(json.dumps({"error": "未找到任何会话文件"}, ensure_ascii=False))
        return []

    results = []
    # 去重：同一个文件路径只取最新的（按 mtime 最大）
    seen = set()
    unique = []
    for tool, path, mtime, size in sessions:
        if path not in seen:
            seen.add(path)
            unique.append((tool, path, mtime, size))

    for i, (tool, path, _mtime, _size) in enumerate(unique[:limit]):
        meta = get_cached_meta(path)
        turns = extract_qa(path)
        results.append({
            "index": i + 1,
            "tool": tool,
            "title": meta.get("title", "")[:80],
            "start": format_ts(meta.get("start_ts")),
            "end": format_ts(meta.get("end_ts")),
            "duration": format_duration(meta.get("start_ts"), meta.get("end_ts")),
            "turns": len(turns),
            "session_file": os.path.basename(path),
        })

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


def get_session_qa(index):
    """
    提取第 N 个会话（1-based index）的全部 Q&A。
    输出 JSON：{ index, title, tool, turns: [{num, user, assistant}, ...] }
    长文本会被截断（>2000 字符部分用省略号替代）。
    """
    sessions = scan_all_sessions()
    if not sessions:
        print(json.dumps({"error": "未找到任何会话文件"}, ensure_ascii=False))
        return

    # 去重
    seen = set()
    unique = []
    for tool, path, mtime, size in sessions:
        if path not in seen:
            seen.add(path)
            unique.append((tool, path, mtime, size))

    idx = int(index) - 1
    if idx < 0 or idx >= len(unique):
        print(json.dumps({
            "error": f"索引 {index} 超出范围（共 {len(unique)} 个会话）"
        }, ensure_ascii=False))
        return

    tool, path, _mtime, _size = unique[idx]
    meta = get_cached_meta(path)
    turns = extract_qa(path)

    MAX_TEXT_LEN = 3000  # Q&A 每段最大字符数

    result = {
        "index": index,
        "tool": tool,
        "title": meta.get("title", "")[:80],
        "session_file": os.path.basename(path),
        "start": format_ts(meta.get("start_ts")),
        "end": format_ts(meta.get("end_ts")),
        "turns": [],
    }

    for t in turns:
        user_text = t["user"]
        assistant_text = t.get("assistant", "")

        if len(user_text) > MAX_TEXT_LEN:
            user_text = user_text[:MAX_TEXT_LEN] + f"\n\n…[截断，原始 {len(t['user'])} 字符]"
        if len(assistant_text) > MAX_TEXT_LEN:
            assistant_text = assistant_text[:MAX_TEXT_LEN] + f"\n\n…[截断，原始 {len(t.get('assistant', ''))} 字符]"

        result["turns"].append({
            "num": t["num"],
            "user": user_text,
            "assistant": assistant_text,
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def slugify(text):
    """中文友好 slug：保留中文字符，英文转小写，空格/标点转连字符"""
    import re
    # 中文字符、字母、数字保留，其余转 -
    slug = re.sub(r'[^一-鿿\w]', '-', text.lower())
    slug = re.sub(r'-{2,}', '-', slug)
    slug = slug.strip('-')
    return slug[:60] if slug else "untitled"


def write_card(card_json_str):
    """
    将一张知识卡片写入 memory 目录。
    参数为 JSON 字符串。
    文件名格式：kb_{维度}_{slug}.md
    """
    try:
        card = json.loads(card_json_str)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON 解析失败: {e}"}, ensure_ascii=False))
        return

    required = ["name", "description"]
    for key in required:
        if key not in card:
            print(json.dumps({"error": f"缺少必填字段: {key}"}, ensure_ascii=False))
            return

    name = card["name"]
    description = card["description"]
    dimensions = card.get("dimensions", [])
    tags = card.get("tags", [])
    source_session = card.get("source_session", "")
    source_turn = card.get("source_turn", "")
    body = card.get("body", "")
    created = card.get("created", datetime.now().strftime("%Y-%m-%d"))

    # 生成文件名
    dim_prefix = dimensions[0] if dimensions else "general"
    slug = slugify(name)
    filename = f"kb_{dim_prefix}_{slug}.md"
    filepath = os.path.join(MEMORY_DIR, filename)

    # 去重：如果同名文件已存在，加数字后缀
    base = filepath
    counter = 1
    while os.path.exists(filepath):
        stem = base[:-3]  # 去掉 .md
        filepath = f"{stem}-{counter}.md"
        counter += 1

    # 构建文件内容
    dims_json = json.dumps(dimensions, ensure_ascii=False)
    tags_json = json.dumps(tags, ensure_ascii=False)

    content = f"""---
name: {name}
description: {description}
type: knowledge
dimensions: {dims_json}
tags: {tags_json}
source:
  - session: {source_session}
    turn: {source_turn}
created: {created}
status: confirmed
---

{body}

---
*来源: [{source_session}]*"""

    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(json.dumps({
        "ok": True,
        "file": filepath,
        "name": name,
    }, ensure_ascii=False))


def update_index():
    """
    扫描 memory 目录下所有 .md 文件（排除 MEMORY.md），
    读取 frontmatter 中的 name 和 description，重建 MEMORY.md 索引。
    """
    import re

    if not os.path.isdir(MEMORY_DIR):
        print(json.dumps({"error": f"memory 目录不存在: {MEMORY_DIR}"}, ensure_ascii=False))
        return

    entries = []
    for fname in sorted(os.listdir(MEMORY_DIR)):
        if fname == "MEMORY.md" or not fname.endswith(".md"):
            continue

        fpath = os.path.join(MEMORY_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        # 提取 frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            continue

        fm_text = fm_match.group(1)
        name_match = re.search(r'name:\s*(.*)', fm_text)
        desc_match = re.search(r'description:\s*(.*)', fm_text)

        name = name_match.group(1).strip() if name_match else fname
        desc = desc_match.group(1).strip() if desc_match else ""

        entries.append((fname, name, desc))

    # 构建 MEMORY.md
    lines = ["# Memory Index\n"]
    for fname, name, desc in entries:
        if desc:
            lines.append(f"- [{name}]({fname}) — {desc}")
        else:
            lines.append(f"- [{name}]({fname})")

    index_path = os.path.join(MEMORY_DIR, "MEMORY.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(json.dumps({
        "ok": True,
        "file": index_path,
        "entries": len(entries),
    }, ensure_ascii=False))


# ═══════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="知识库助手")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", parents=[
        argparse.ArgumentParser(add_help=False)
    ]).add_argument("--limit", type=int, default=15)

    p_qa = sub.add_parser("qa")
    p_qa.add_argument("index", type=int)

    p_card = sub.add_parser("write-card")
    p_card.add_argument("json", type=str)

    sub.add_parser("update-index")

    args = parser.parse_args()

    if args.command == "list":
        list_sessions(limit=args.limit)
    elif args.command == "qa":
        get_session_qa(args.index)
    elif args.command == "write-card":
        write_card(args.json)
    elif args.command == "update-index":
        update_index()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
