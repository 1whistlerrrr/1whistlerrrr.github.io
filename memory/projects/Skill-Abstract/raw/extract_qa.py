#!/usr/bin/env python3
"""
从 Claude Code / Codex 会话 JSONL 提取用户提问 + AI 最终回答。
跳过思考、工具调用、系统注入。输出干净 Markdown。

用法：
  python3 extract_qa.py                    # 最新会话
  python3 extract_qa.py --list             # 列出所有会话（第一个有效提问作为标题）
  python3 extract_qa.py <id>               # 指定会话
  python3 extract_qa.py <id> -o out.md     # 指定输出
"""
import json, os, glob, re, argparse
from datetime import datetime

TOOL_SOURCES = [
    ("Claude Code", "~/.claude/projects", "*/*.jsonl"),
    ("Codex",       "~/.codex/sessions",      "*/*/*/*.jsonl"),
    ("Codex(归档)", "~/.codex/archived_sessions", "*.jsonl"),
]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
_CACHE_FILE = os.path.join(OUTPUT_DIR, ".first_question_cache.json")

SKIP_PREFIXES = [
    "Base directory for this skill:",
    "STEP 0:", "# STEP 0:",
    "SKILL CONTRACT", "# SKILL CONTRACT",
    "OUTPUT CONTRACT", "# OUTPUT CONTRACT",
    "HOW TO INVOKE", "# HOW TO INVOKE",
    "last30days v", "# last30days",
]

# ═══════════════════════════════════════════════════════
# 标题清洗
# ═══════════════════════════════════════════════════════

def clean_title(raw):
    """清洗第一个提问，输出 ≤60 字符的可读标题"""
    # 1. 提取 <command-args>（用户真正输入）
    m = re.search(r'<command-args>(.*?)</command-args>', raw, re.DOTALL)
    if m:
        raw = m.group(1).strip()

    # 2. 去 XML 标签
    raw = re.sub(r'<[^>]+>', '', raw)

    # 3. 去系统提示
    raw = re.sub(r'Caveat:.*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'DO NOT respond to these messages.*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'The user opened the file\s*', '', raw)
    raw = re.sub(r'The user selected the lines \d+ to \d+ from\s*', '', raw)
    raw = re.sub(r'\s*in the IDE\.\s*This may or may not be (?:related|relevant).*$', '', raw)
    raw = re.sub(r'\s*This may or may not be (?:related|relevant).*?\.(?=\s|$)', '', raw)
    #    去 task-notification 类系统消息
    raw = re.sub(r'^call_\S+\s+.*?(?:killed|stopped|completed).*?\.(?=\s|$)', '', raw)

    # 4. 去 skill 调用前缀 "ponytail:review /ponytail:review"
    raw = re.sub(r'^\S+:\S+\s+/\S+:\S+\s*', '', raw)

    # 5. 缩短路径 /Users/.../file.ext → file.ext
    raw = re.sub(r'(?:根据|查看|在|文件\s*)?/Users/\S+?/([^/\s]+?\.[a-z0-9]{1,8})', r'\1', raw)
    raw = re.sub(r'(?:根据|查看|在|文件\s*)?/Users/\S{30,}', '', raw)
    raw = re.sub(r'(?:根据|查看|在)?\S+?/([^/\s]+?\.[a-z0-9]{1,8})\s+in the IDE', r'\1', raw)

    # 6. 合并空白、去标点残留
    raw = re.sub(r'\s+', ' ', raw).strip()
    raw = raw.lstrip('，,。. ')

    return raw if len(raw) >= 3 else ""

# ═══════════════════════════════════════════════════════
# 第一个有效提问
# ═══════════════════════════════════════════════════════

def is_skill_injection(text):
    for p in SKIP_PREFIXES:
        if text.strip().startswith(p):
            return True
    return len(text) > 2000 and ("Pre-Flight Checklist" in text or "Pre-Research Intelligence" in text)

def first_question(filepath):
    """读 JSONL 前 300 行，找第一个清洗后有效的用户提问"""
    try:
        found_raw = []
        with open(filepath) as f:
            for i, line in enumerate(f):
                if i > 300:
                    break
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("message", {}).get("role") != "user":
                    continue
                content = row["message"].get("content", "")
                texts = []
                if isinstance(content, str):
                    texts = [content.strip()]
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            t = item.get("text", "").strip()
                            if t: texts.append(t)
                        elif isinstance(item, str) and item.strip():
                            texts.append(item.strip())
                texts = [t for t in texts if not is_skill_injection(t)]
                for t in texts:
                    c = clean_title(t)
                    if c:
                        return c
                    found_raw.append(t)
        # 所有都清洗为空 → 取第一个原始文本截断
        if found_raw:
            r = re.sub(r'<[^>]+>', '', found_raw[0])
            r = re.sub(r'\s+', ' ', r).strip()
            return r[:60] if r else ""
    except Exception:
        pass
    return ""

# ═══════════════════════════════════════════════════════
# 缓存
# ═══════════════════════════════════════════════════════

def _load_cache():
    try:
        with open(_CACHE_FILE) as f:
            return json.load(f)
    except:
        return {}

def _save_cache(c):
    try:
        with open(_CACHE_FILE, 'w') as f:
            json.dump(c, f)
    except:
        pass

def get_title(filepath):
    cache = _load_cache()
    try:
        st = os.stat(filepath)
        key = f"{os.path.basename(filepath)}:{st.st_mtime}:{st.st_size}"
    except:
        key = os.path.basename(filepath)
    if key not in cache:
        cache[key] = first_question(filepath) or "(无有效提问)"
        _save_cache(cache)
    return cache[key]

# ═══════════════════════════════════════════════════════
# 扫描 & 列表
# ═══════════════════════════════════════════════════════

def scan_all_sessions():
    results = []
    for tool, root, pattern in TOOL_SOURCES:
        fp = os.path.join(os.path.expanduser(root), pattern)
        for f in glob.glob(fp):
            results.append((tool, f, os.path.getmtime(f), os.path.getsize(f)))
    results.sort(key=lambda x: x[2], reverse=True)
    return results

def list_sessions():
    sessions = scan_all_sessions()
    if not sessions:
        print("未找到任何会话文件")
        return
    print(f"{'时间':<17} {'大小':>8}  {'工具':<14}  {'标题（第一个有效提问）'}")
    print("-" * 110)
    for tool, path, mtime, size in sessions:
        ts = datetime.fromtimestamp(mtime).strftime("%m-%d %H:%M")
        title = get_title(path)
        sid = os.path.splitext(os.path.basename(path))[0]
        if len(sid) > 16:
            sid = sid[:13] + "..."
        print(f"{ts:<17} {size:>8,}  {tool:<14}  {title:<55} {sid}")

def find_session(sid=None):
    sessions = scan_all_sessions()
    if not sessions:
        raise SystemExit("未找到会话")
    if sid:
        for tool, path, _, _ in sessions:
            if sid in os.path.basename(path):
                return tool, path
        raise SystemExit(f"未找到 '{sid}'")
    return sessions[0][0], sessions[0][1]

# ═══════════════════════════════════════════════════════
# 提取
# ═══════════════════════════════════════════════════════

def get_text_parts(content):
    if isinstance(content, str):
        return [content.strip()] if content.strip() else []
    parts = []
    for item in (content if isinstance(content, list) else []):
        if isinstance(item, dict) and item.get("type") == "text":
            t = item.get("text", "").strip()
            if t: parts.append(t)
        elif isinstance(item, str) and item.strip():
            parts.append(item.strip())
    return parts

def extract_qa(path):
    turns = []
    u_parts, a_final = [], ""
    active = False

    with open(path) as f:
        for line in f:
            try: row = json.loads(line)
            except: continue
            msg = row.get("message", {})
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                texts = [t for t in get_text_parts(content) if not is_skill_injection(t)] if isinstance(content, list) else (
                    [content.strip()] if isinstance(content, str) and content.strip() and not is_skill_injection(content) else []
                )
                if texts:
                    if active and a_final:
                        turns.append({"num": len(turns)+1, "user": "\n\n".join(u_parts), "assistant": a_final})
                    u_parts, a_final = texts, ""
                    active = True
            elif role == "assistant" and isinstance(content, list):
                t = get_text_parts(content)
                if t: a_final = "\n\n".join(t)

    if active and a_final:
        turns.append({"num": len(turns)+1, "user": "\n\n".join(u_parts), "assistant": a_final})
    return turns

# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="提取 AI 编码工具会话问答")
    p.add_argument("session", nargs="?", help="会话 ID 或前缀")
    p.add_argument("-o", "--output", help="输出文件路径")
    p.add_argument("--list", action="store_true", help="列出所有会话")
    a = p.parse_args()

    if a.list:
        list_sessions()
        return

    tool, path = find_session(a.session)
    turns = extract_qa(path)

    out = a.output or os.path.join(OUTPUT_DIR, f"session-qa-{os.path.splitext(os.path.basename(path))[0][:8]}.md")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    with open(out, 'w') as f:
        dt = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
        f.write(f"# 对话记录（仅最终问答）\n\n**来源**: {tool}  |  **时间**: {dt}  |  **总轮次**: {len(turns)}\n\n---\n\n")
        for t in turns:
            u = t['user']
            if len(u) > 3000:
                u = u[:500] + f"\n\n…[截短：原始 {len(t['user'])} 字符]\n"
            f.write(f"## 第 {t['num']} 轮\n\n**👤 提问**\n\n{u}\n\n**🤖 回答**\n\n{t['assistant']}\n\n---\n\n")

    total = sum(len(t['user'])+len(t['assistant']) for t in turns)
    print(f"✅ {out}")
    print(f"   来源: {tool}  |  轮次: {len(turns)}  |  字符: {total:,}  |  大小: {os.path.getsize(out):,} bytes")

if __name__ == "__main__":
    main()
