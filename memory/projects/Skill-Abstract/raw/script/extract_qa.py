#!/usr/bin/env python3
"""
从 Claude Code / Codex 会话 JSONL 中提取用户提问 + AI 最终回答，
跳过思考过程、工具调用、系统注入内容。输出干净 Markdown。

用法：
  python3 extract_qa.py                          # 最新会话
  python3 extract_qa.py --list                   # 列出所有可用会话（每个会话用第一个提问作为标题）
  python3 extract_qa.py <id>                     # 指定会话（支持 UUID 前缀、Codex rollout 名）
  python3 extract_qa.py <id> -o out.md           # 指定输出文件
"""
import json, os, glob, argparse
from datetime import datetime

TOOL_SOURCES = [
    ("Claude Code", "~/.claude/projects", "*/*.jsonl"),
    ("Codex",       "~/.codex/sessions",      "*/*/*/*.jsonl"),
    ("Codex(归档)", "~/.codex/archived_sessions", "*.jsonl"),
]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

SKIP_PREFIXES = [
    "Base directory for this skill:",
    "STEP 0:", "# STEP 0:",
    "SKILL CONTRACT", "# SKILL CONTRACT",
    "OUTPUT CONTRACT", "# OUTPUT CONTRACT",
    "HOW TO INVOKE", "# HOW TO INVOKE",
    "last30days v", "# last30days",
]

# ── 第一个提问（用作标题） ───────────────────────────
def is_skill_injection(text):
    for prefix in SKIP_PREFIXES:
        if text.strip().startswith(prefix):
            return True
    if len(text) > 2000:
        if "Pre-Flight Checklist" in text or "Pre-Research Intelligence" in text:
            return True
    return False

def first_question(filepath):
    """打开 JSONL，找到第一个清洗后有效的用户提问。只读前 ~300 行。
    如果一个用户消息清洗后为空（如纯 skill 调用），继续往下找。"""
    try:
        found_raw = []
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if i > 300:
                    break
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = row.get("message", {})
                if msg.get("role") != "user":
                    continue
                content = msg.get("content", "")
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
        # 所有都清洗为空 → 取第一个原始文本截断兜底
        if found_raw:
            r = re.sub(r'<[^>]+>', '', found_raw[0])
            r = re.sub(r'\s+', ' ', r).strip()
            return r[:60] if r else ""
    except Exception:
        pass
    return ""

# ── 标题清洗 ────────────────────────────────────────
import re

def clean_title(raw):
    """把第一个提问清洗成人可读的短标题"""
    # 1. 优先提取 <command-args>
    m = re.search(r'<command-args>(.*?)</command-args>', raw, re.DOTALL)
    if m:
        raw = m.group(1).strip()

    # 2. 去 XML
    raw = re.sub(r'<[^>]+>', '', raw)

    # 3. 去系统提示
    raw = re.sub(r'Caveat:.*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'DO NOT respond to these messages.*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'The user opened the file\s*', '', raw)
    raw = re.sub(r'The user selected the lines \d+ to \d+ from\s*', '', raw)
    raw = re.sub(r'\s*in the IDE\.\s*This may or may not be (?:related|relevant).*$', '', raw)
    raw = re.sub(r'\s*This may or may not be (?:related|relevant).*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'^call_\S+\s+.*?(?:killed|stopped|completed).*?\.(?=\s|$)', '', raw)

    # 4. 去 skill 调用前缀
    raw = re.sub(r'^\S+:\S+\s+/\S+:\S+\s*', '', raw)

    # 5. 缩短路径：/Users/.../file.ext → file.ext
    raw = re.sub(r'(?:根据|查看|在|文件\s*)?/Users/\S+?/([^/\s]+?\.[a-z0-9]{1,8})', r'\1', raw)
    raw = re.sub(r'(?:根据|查看|在|文件\s*)?/Users/\S{30,}', '', raw)
    #    也处理非 /Users 开头的仓库路径（如 xxx.github.io/CLAUDE.md）
    raw = re.sub(r'(?:根据|查看|在)?\S+?/([^/\s]+?\.[a-z0-9]{1,8})\s+in the IDE', r'\1', raw)

    # 6. 合并空白
    raw = re.sub(r'\s+', ' ', raw).strip()

    # 7. 去掉开头的标点残留
    raw = raw.lstrip('，,。. ')

    # 8. 如果清洗后只剩标点或空
    if not raw or len(raw) < 3:
        return ""

    if len(raw) > 60:
        raw = raw[:57] + "..."

    return raw

# ── 缓存 ────────────────────────────────────────────
_CACHE_FILE = os.path.join(OUTPUT_DIR, ".first_question_cache.json")

def _load_cache():
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {}

def _save_cache(cache):
    try:
        with open(_CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except:
        pass

def get_title(filepath):
    """取第一个提问作为标题，截断到 60 字符，缓存结果"""
    cache = _load_cache()
    # 用文件 mtime + size 作为缓存 key
    try:
        stat = os.stat(filepath)
        key = f"{os.path.basename(filepath)}:{stat.st_mtime}:{stat.st_size}"
    except:
        key = os.path.basename(filepath)

    if key in cache:
        return cache[key]

    q = clean_title(first_question(filepath))
    cache[key] = q
    _save_cache(cache)
    return q

# ── 扫描 ────────────────────────────────────────────
def scan_all_sessions():
    """返回 [(工具名, 路径, mtime, 大小)]"""
    results = []
    for tool, root, pattern in TOOL_SOURCES:
        full_pattern = os.path.join(os.path.expanduser(root), pattern)
        for f in glob.glob(full_pattern):
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
        # if len(sid) > 16:
        #     sid = sid[:13] + "..."
        print(f"{ts:<17} {size:>8,}  {tool:<14}  {sid}  {title:<55}")

def find_session(session_id=None):
    sessions = scan_all_sessions()
    if not sessions:
        raise SystemExit("未找到任何会话文件")
    if session_id:
        for tool, path, _, _ in sessions:
            if session_id in os.path.basename(path):
                return tool, path
        raise SystemExit(f"未找到匹配 '{session_id}' 的会话")
    else:
        return sessions[0][0], sessions[0][1]

# ── 提取逻辑 ────────────────────────────────────────
def get_text_parts(content):
    if isinstance(content, str):
        return [content.strip()] if content.strip() else []
    texts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            t = item.get("text", "").strip()
            if t: texts.append(t)
        elif isinstance(item, str):
            t = item.strip()
            if t: texts.append(t)
    return texts

def extract_qa(session_file):
    turns = []
    current_user_parts = []
    current_final_answer = ""
    in_turn = False

    with open(session_file, 'r') as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = row.get("message", {})
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                if isinstance(content, list):
                    texts = [t for t in get_text_parts(content) if not is_skill_injection(t)]
                    if texts:
                        if in_turn and current_final_answer:
                            turns.append({"num": len(turns)+1, "user": "\n\n".join(current_user_parts), "assistant": current_final_answer})
                        current_user_parts = texts
                        current_final_answer = ""
                        in_turn = True
                elif isinstance(content, str) and content.strip():
                    if not is_skill_injection(content):
                        if in_turn and current_final_answer:
                            turns.append({"num": len(turns)+1, "user": "\n\n".join(current_user_parts), "assistant": current_final_answer})
                        current_user_parts = [content.strip()]
                        current_final_answer = ""
                        in_turn = True

            elif role == "assistant":
                if isinstance(content, list):
                    texts = get_text_parts(content)
                    if texts:
                        current_final_answer = "\n\n".join(texts)

    if in_turn and current_final_answer:
        turns.append({"num": len(turns)+1, "user": "\n\n".join(current_user_parts), "assistant": current_final_answer})
    return turns

# ── 主入口 ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="提取 AI 编码工具会话问答")
    parser.add_argument("session", nargs="?", help="会话 ID 或前缀")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--list", action="store_true", help="列出所有可用会话")
    args = parser.parse_args()

    if args.list:
        list_sessions()
        return

    tool_name, session_file = find_session(args.session)
    turns = extract_qa(session_file)

    if args.output:
        output_file = args.output
    else:
        sid = os.path.splitext(os.path.basename(session_file))[0][:8]
        output_file = os.path.join(OUTPUT_DIR, f"session-qa-{sid}.md")

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    with open(output_file, 'w') as f:
        session_date = datetime.fromtimestamp(os.path.getmtime(session_file)).strftime("%Y-%m-%d %H:%M")
        f.write(f"# 对话记录（仅最终问答）\n\n")
        f.write(f"**来源**: {tool_name}  |  **时间**: {session_date}  |  **总轮次**: {len(turns)}\n\n")
        f.write("---\n\n")
        for t in turns:
            user_text = t['user']
            if len(user_text) > 3000:
                user_text = user_text[:500] + f"\n\n…[截短：原始 {len(t['user'])} 字符]\n"
            f.write(f"## 第 {t['num']} 轮\n\n")
            f.write(f"**👤 提问**\n\n{user_text}\n\n")
            f.write(f"**🤖 回答**\n\n{t['assistant']}\n\n")
            f.write("---\n\n")

    total_chars = sum(len(t['user'])+len(t['assistant']) for t in turns)
    print(f"✅ 导出完成: {output_file}")
    print(f"   来源工具: {tool_name}")
    print(f"   总轮次: {len(turns)}")
    print(f"   总字符: {total_chars:,}")
    print(f"   文件大小: {os.path.getsize(output_file):,} bytes")

if __name__ == "__main__":
    main()
