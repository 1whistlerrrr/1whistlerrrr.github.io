#!/usr/bin/env python3
"""
从 Claude Code / Codex 会话 JSONL 中提取用户提问 + AI 最终回答，
跳过思考过程、工具调用、系统注入内容。输出干净 Markdown。

用法：
  python3 extract_qa.py                              # 最新会话
  python3 extract_qa.py --list                       # 列出所有可用会话（含开始/结束时间）
  python3 extract_qa.py <id>                         # 指定会话（支持 UUID 前缀、Codex rollout 名）
  python3 extract_qa.py <id> -o out.md               # 指定输出文件
  python3 extract_qa.py <id> --user-only             # 只输出用户提问
  python3 extract_qa.py --select                     # 交互式选择多个会话批量导出（分开文件）
  python3 extract_qa.py --select --merge             # 交互式选择，合并输出到单个文件
  python3 extract_qa.py --select --user-only         # 批量导出，仅用户提问
"""
import json, os, glob, argparse, sys, re, unicodedata
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

# ═══════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════

def display_width(s):
    """计算字符串的终端显示宽度（CJK 字符占 2 列）"""
    w = 0
    for c in s:
        w += 2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1
    return w


def cjk_ljust(s, width):
    """左对齐到指定显示宽度，正确处理 CJK 全角字符"""
    return s + ' ' * max(0, width - display_width(s))


# ═══════════════════════════════════════════════════════════
#  时间戳提取
# ═══════════════════════════════════════════════════════════

TIMESTAMP_FIELDS = ['timestamp', 'ts', 'created_at', 'time', 'createdAt', 'iso_timestamp']


def parse_timestamp(val):
    """解析各种时间戳格式 → Unix float，失败返回 None"""
    if isinstance(val, (int, float)):
        if val > 1e12:          # 毫秒
            return val / 1000.0
        return float(val)
    if isinstance(val, str):
        val = val.strip()
        if not val:
            return None
        # 纯数字字符串
        try:
            v = float(val)
            if v > 1e12:
                return v / 1000.0
            return v
        except ValueError:
            pass
        # ISO 8601
        try:
            return datetime.fromisoformat(val.replace('Z', '+00:00')).timestamp()
        except (ValueError, TypeError):
            pass
        # 常见变体：2024-01-15 09:30:00
        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y/%m/%d %H:%M:%S']:
            try:
                return datetime.strptime(val, fmt).timestamp()
            except ValueError:
                continue
    return None


def extract_timestamp(row):
    """从 JSONL 行中提取时间戳（先 row 级，再 message 级）"""
    for field in TIMESTAMP_FIELDS:
        val = row.get(field)
        ts = parse_timestamp(val)
        if ts is not None:
            return ts

    msg = row.get('message', {})
    if isinstance(msg, dict):
        for field in TIMESTAMP_FIELDS:
            val = msg.get(field)
            ts = parse_timestamp(val)
            if ts is not None:
                return ts
    return None


def get_session_time_range(filepath):
    """
    读取 JSONL 文件的第一条和最后一条消息时间戳。
    返回 (start_ts, end_ts)，均为 Unix float；失败返回 (None, None)。
    """
    try:
        start_ts = None
        end_ts = None

        with open(filepath, 'rb') as f:
            # ── 开始时间：读前若干行直到找到有效时间戳 ──
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                try:
                    row = json.loads(line.decode('utf-8', errors='replace'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
                ts = extract_timestamp(row)
                if ts is not None:
                    start_ts = ts
                    break

            # ── 结束时间：从文件末尾往前读 ──
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            if file_size == 0:
                return start_ts, None

            chunk_size = min(65536, file_size)
            f.seek(max(0, file_size - chunk_size))
            tail = f.read()

            lines = tail.decode('utf-8', errors='replace').strip().split('\n')
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = extract_timestamp(row)
                if ts is not None:
                    end_ts = ts
                    break

        return start_ts, end_ts
    except Exception:
        return None, None


def format_ts(ts):
    """Unix timestamp → 'MM-DD HH:MM' 字符串"""
    if ts is None:
        return "?              "
    return datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")


def format_duration(start_ts, end_ts):
    """两个 Unix timestamp 的差值 → 人类可读时长"""
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
    if m == 0:
        return f"{h}h"
    return f"{h}h{m:02d}m"


# ═══════════════════════════════════════════════════════════
#  标题提取（与原版一致）
# ═══════════════════════════════════════════════════════════

def is_skill_injection(text):
    for prefix in SKIP_PREFIXES:
        if text.strip().startswith(prefix):
            return True
    if len(text) > 2000:
        if "Pre-Flight Checklist" in text or "Pre-Research Intelligence" in text:
            return True
    return False


def first_question(filepath):
    """打开 JSONL，找到第一个清洗后有效的用户提问。只读前 ~300 行。"""
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
                            if t:
                                texts.append(t)
                        elif isinstance(item, str) and item.strip():
                            texts.append(item.strip())
                texts = [t for t in texts if not is_skill_injection(t)]
                for t in texts:
                    c = clean_title(t)
                    if c:
                        return c
                    found_raw.append(t)
        if found_raw:
            r = re.sub(r'<[^>]+>', '', found_raw[0])
            r = re.sub(r'\s+', ' ', r).strip()
            return r[:60] if r else ""
    except Exception:
        pass
    return ""


def clean_title(raw):
    """把第一个提问清洗成人可读的短标题"""
    m = re.search(r'<command-args>(.*?)</command-args>', raw, re.DOTALL)
    if m:
        raw = m.group(1).strip()

    raw = re.sub(r'<[^>]+>', '', raw)
    raw = re.sub(r'Caveat:.*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'DO NOT respond to these messages.*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'The user opened the file\s*', '', raw)
    raw = re.sub(r'The user selected the lines \d+ to \d+ from\s*', '', raw)
    raw = re.sub(r'\s*in the IDE\.\s*This may or may not be (?:related|relevant).*$', '', raw)
    raw = re.sub(r'\s*This may or may not be (?:related|relevant).*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'^call_\S+\s+.*?(?:killed|stopped|completed).*?\.(?=\s|$)', '', raw)
    raw = re.sub(r'^\S+:\S+\s+/\S+:\S+\s*', '', raw)
    raw = re.sub(r'(?:根据|查看|在|文件\s*)?/Users/\S+?/([^/\s]+?\.[a-z0-9]{1,8})', r'\1', raw)
    raw = re.sub(r'(?:根据|查看|在|文件\s*)?/Users/\S{30,}', '', raw)
    raw = re.sub(r'(?:根据|查看|在)?\S+?/([^/\s]+?\.[a-z0-9]{1,8})\s+in the IDE', r'\1', raw)
    raw = re.sub(r'\s+', ' ', raw).strip()
    raw = raw.lstrip('，,。. ')
    if not raw or len(raw) < 3:
        return ""
    if len(raw) > 60:
        raw = raw[:57] + "..."
    return raw


# ═══════════════════════════════════════════════════════════
#  缓存（扩展：同时存 start/end 时间）
# ═══════════════════════════════════════════════════════════

_CACHE_FILE = os.path.join(OUTPUT_DIR, ".first_question_cache.json")


def _load_cache():
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_cache(cache):
    try:
        with open(_CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception:
        pass


def _file_key(filepath):
    try:
        stat = os.stat(filepath)
        return f"{os.path.basename(filepath)}:{stat.st_mtime}:{stat.st_size}"
    except Exception:
        return os.path.basename(filepath)


def get_cached_meta(filepath):
    """
    返回 {title, start_ts, end_ts}，若未缓存则全部计算并写入缓存。
    兼容旧缓存格式（纯字符串 title）。
    """
    cache = _load_cache()
    key = _file_key(filepath)

    if key in cache:
        val = cache[key]
        if isinstance(val, dict) and 'title' in val:
            return val
        if isinstance(val, str):
            # 旧格式：title 已有，补提取时间并升级缓存
            title = val
            start_ts, end_ts = get_session_time_range(filepath)
            meta = {'title': title, 'start_ts': start_ts, 'end_ts': end_ts}
            cache[key] = meta
            _save_cache(cache)
            return meta

    # 计算并缓存
    title = clean_title(first_question(filepath))
    start_ts, end_ts = get_session_time_range(filepath)

    meta = {'title': title, 'start_ts': start_ts, 'end_ts': end_ts}
    cache[key] = meta
    _save_cache(cache)
    return meta


def get_title(filepath):
    """取第一个提问作为标题（兼容旧接口）"""
    return get_cached_meta(filepath)['title']


# ═══════════════════════════════════════════════════════════
#  扫描
# ═══════════════════════════════════════════════════════════

def scan_all_sessions():
    """返回 [(工具名, 路径, mtime, 大小)]"""
    results = []
    for tool, root, pattern in TOOL_SOURCES:
        full_pattern = os.path.join(os.path.expanduser(root), pattern)
        for f in glob.glob(full_pattern):
            results.append((tool, f, os.path.getmtime(f), os.path.getsize(f)))
    results.sort(key=lambda x: x[2], reverse=True)
    return results


def list_sessions(show_index=False):
    """
    列出所有会话，包含开始时间、结束时间、时长。
    show_index=True 时显示序号列（供 --select 使用）。
    """
    sessions = scan_all_sessions()
    if not sessions:
        print("未找到任何会话文件")
        return sessions

    # 表头（用 CJK 感知的左对齐）
    if show_index:
        header = (f"{'#':<4} {cjk_ljust('开始时间', 12)} {cjk_ljust('结束时间', 12)} "
                  f"{cjk_ljust('时长', 7)} {'大小':>7}  {cjk_ljust('工具', 14)}  {'标题'}")
    else:
        header = (f"{cjk_ljust('开始时间', 12)} {cjk_ljust('结束时间', 12)} "
                  f"{cjk_ljust('时长', 7)} {'大小':>7}  {cjk_ljust('工具', 14)}  {'标题'}")
    print(header)
    print("-" * display_width(header))

    for idx, (tool, path, _mtime, size) in enumerate(sessions):
        meta = get_cached_meta(path)
        start = format_ts(meta.get('start_ts'))
        end = format_ts(meta.get('end_ts'))
        dur = format_duration(meta.get('start_ts'), meta.get('end_ts'))
        title = meta.get('title', '')

        if show_index:
            print(f"{idx + 1:<4} {start:<12} {end:<12} {cjk_ljust(dur, 7)} {size:>7,}  {cjk_ljust(tool, 14)}  {title}")
        else:
            print(f"{start:<12} {end:<12} {cjk_ljust(dur, 7)} {size:>7,}  {cjk_ljust(tool, 14)}  {title}")

    return sessions


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


# ═══════════════════════════════════════════════════════════
#  交互式选择
# ═══════════════════════════════════════════════════════════

def parse_range(input_str, max_idx):
    """
    解析 "1,3,5-8" 或 "all" → 0-based 索引列表（去重排序）。
    输入序号是 1-based，输出 0-based。
    """
    s = input_str.strip()
    if s.lower() == 'all' or s.lower() == 'a':
        return list(range(max_idx))

    selected = set()
    parts = re.split(r'[,，\s]+', s)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                a, b = int(a.strip()), int(b.strip())
                for i in range(a, b + 1):
                    if 1 <= i <= max_idx:
                        selected.add(i - 1)
            except ValueError:
                print(f"  ⚠ 跳过无效范围: {part}")
        else:
            try:
                i = int(part)
                if 1 <= i <= max_idx:
                    selected.add(i - 1)
            except ValueError:
                print(f"  ⚠ 跳过无效输入: {part}")

    return sorted(selected)


def select_sessions(args):
    """交互式选择会话并批量导出。args.merge 控制分开/合并输出。"""
    sessions = list_sessions(show_index=True)

    if not sessions:
        return

    print()
    if args.merge:
        print("输入要导出的会话编号，如: 1,3,5-8 或 all（合并到单个文件，直接回车取消）")
    else:
        print("输入要导出的会话编号，如: 1,3,5-8 或 all（分开输出，直接回车取消）")
    try:
        user_input = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消")
        return

    if not user_input:
        print("已取消")
        return

    indices = parse_range(user_input, len(sessions))
    if not indices:
        print("未选中任何会话")
        return

    print(f"\n将导出 {len(indices)} 个会话：")
    for i in indices:
        meta = get_cached_meta(sessions[i][1])
        print(f"  #{i + 1}  {meta.get('title', '(无标题)')[:50]}")
    print()

    # ── 合并模式：所有会话写入单个文件 ──
    if args.merge:
        out_file = args.output if args.output else os.path.join(OUTPUT_DIR, "session-qa-merged.md")
        out_file = os.path.expanduser(out_file)
        os.makedirs(os.path.dirname(out_file) or ".", exist_ok=True)

        total_turns = 0
        with open(out_file, 'w') as f:
            if args.user_only:
                f.write(f"# 批量对话记录（仅用户提问）\n\n")
            else:
                f.write(f"# 批量对话记录（仅最终问答）\n\n")
            f.write(f"**会话数**: {len(indices)}  |  **模式**: 合并输出\n\n")
            f.write("---\n\n")

            for session_idx, i in enumerate(indices, 1):
                tool, path, _mtime, _size = sessions[i]
                meta = get_cached_meta(path)
                turns = extract_qa(path)
                total_turns += len(turns)

                start_str = format_ts(meta.get('start_ts'))
                end_str = format_ts(meta.get('end_ts'))
                title = meta.get('title', '')

                f.write(f"## 会话 {session_idx}\n\n")
                f.write(f"**来源**: {tool}  |  **时间**: {start_str} → {end_str}")
                f.write(f"  |  **标题**: {title}")
                f.write(f"  |  **轮次**: {len(turns)}\n\n")
                f.write("---\n\n")

                for t in turns:
                    user_text = t['user']
                    if len(user_text) > 3000:
                        user_text = user_text[:500] + f"\n\n…[截短：原始 {len(t['user'])} 字符]\n"
                    f.write(f"### 第 {t['num']} 轮\n\n")
                    f.write(f"**👤 提问**\n\n{user_text}\n\n")
                    if not args.user_only:
                        f.write(f"**🤖 回答**\n\n{t['assistant']}\n\n")
                    f.write("---\n\n")

                print(f"  ✅ #{i + 1} → 已合并  ({len(turns)} 轮)")

        total_chars = os.path.getsize(out_file)
        print(f"\n完成: {len(indices)} 个会话 → {out_file}")
        print(f"   总轮次: {total_turns}")
        print(f"   文件大小: {total_chars:,} bytes")
        if args.user_only:
            print(f"   模式: 仅用户提问")
        return

    # ── 分开模式：每个会话一个文件 ──
    out_dir = OUTPUT_DIR
    if args.output:
        p = os.path.expanduser(args.output)
        if os.path.isdir(p) or p.endswith(os.sep):
            out_dir = p
        else:
            out_dir = os.path.dirname(p) or "."

    os.makedirs(out_dir, exist_ok=True)

    success = 0
    for i in indices:
        tool, path, _mtime, _size = sessions[i]
        sid = os.path.splitext(os.path.basename(path))[0]
        out_file = os.path.join(out_dir, f"session-qa-{sid[:16]}.md")
        try:
            turns = extract_qa(path)
            write_markdown(out_file, tool, path, turns, user_only=args.user_only)
            print(f"  ✅ #{i + 1} → {os.path.basename(out_file)}  ({len(turns)} 轮)")
            success += 1
        except Exception as e:
            print(f"  ❌ #{i + 1} 失败: {e}")

    print(f"\n完成: {success}/{len(indices)} 个会话已导出 → {out_dir}")


# ═══════════════════════════════════════════════════════════
#  提取逻辑
# ═══════════════════════════════════════════════════════════

def get_text_parts(content):
    if isinstance(content, str):
        return [content.strip()] if content.strip() else []
    texts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            t = item.get("text", "").strip()
            if t:
                texts.append(t)
        elif isinstance(item, str):
            t = item.strip()
            if t:
                texts.append(t)
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
                            turns.append({"num": len(turns) + 1, "user": "\n\n".join(current_user_parts), "assistant": current_final_answer})
                        current_user_parts = texts
                        current_final_answer = ""
                        in_turn = True
                elif isinstance(content, str) and content.strip():
                    if not is_skill_injection(content):
                        if in_turn and current_final_answer:
                            turns.append({"num": len(turns) + 1, "user": "\n\n".join(current_user_parts), "assistant": current_final_answer})
                        current_user_parts = [content.strip()]
                        current_final_answer = ""
                        in_turn = True

            elif role == "assistant":
                if isinstance(content, list):
                    texts = get_text_parts(content)
                    if texts:
                        current_final_answer = "\n\n".join(texts)

    if in_turn and current_final_answer:
        turns.append({"num": len(turns) + 1, "user": "\n\n".join(current_user_parts), "assistant": current_final_answer})
    return turns


# ═══════════════════════════════════════════════════════════
#  输出
# ═══════════════════════════════════════════════════════════

def write_markdown(output_file, tool_name, session_file, turns, user_only=False):
    """写入 Markdown 文件。user_only=True 时仅输出用户提问。"""
    meta = get_cached_meta(session_file)
    start_str = format_ts(meta.get('start_ts'))
    end_str = format_ts(meta.get('end_ts'))

    with open(output_file, 'w') as f:
        if user_only:
            f.write(f"# 对话记录（仅用户提问）\n\n")
        else:
            f.write(f"# 对话记录（仅最终问答）\n\n")
        f.write(f"**来源**: {tool_name}  |  **时间**: {start_str} → {end_str}")
        f.write(f"  |  **总轮次**: {len(turns)}\n\n")
        f.write("---\n\n")

        for t in turns:
            user_text = t['user']
            if len(user_text) > 3000:
                user_text = user_text[:500] + f"\n\n…[截短：原始 {len(t['user'])} 字符]\n"
            f.write(f"# 第 {t['num']} 轮\n\n")
            f.write(f"**👤 提问**\n\n{user_text}\n\n")
            if not user_only:
                f.write(f"**🤖 回答**\n\n{t['assistant']}\n\n")
            f.write("---\n\n")


# ═══════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="提取 AI 编码工具会话问答")
    parser.add_argument("session", nargs="?", help="会话 ID 或前缀")
    parser.add_argument("-o", "--output", help="输出文件路径（--select 模式下为输出目录）")
    parser.add_argument("--list", action="store_true", help="列出所有可用会话（含开始/结束时间）")
    parser.add_argument("--select", action="store_true", help="交互式选择多个会话批量导出")
    parser.add_argument("--merge", action="store_true", help="配合 --select，合并输出到单个文件（默认为分开文件）")
    parser.add_argument("--user-only", action="store_true", help="仅输出用户提问，不输出 AI 回答")
    args = parser.parse_args()

    # ── --select 批量模式 ──
    if args.select:
        select_sessions(args)
        return

    # ── --list 列出会话 ──
    if args.list:
        list_sessions()
        return

    # ── 单会话导出 ──
    tool_name, session_file = find_session(args.session)
    turns = extract_qa(session_file)

    if args.output:
        output_file = args.output
    else:
        sid = os.path.splitext(os.path.basename(session_file))[0][:8]
        output_file = os.path.join(OUTPUT_DIR, f"session-qa-{sid}.md")

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    write_markdown(output_file, tool_name, session_file, turns, user_only=args.user_only)

    total_chars = sum(len(t['user']) + len(t.get('assistant', '')) for t in turns)
    print(f"✅ 导出完成: {output_file}")
    print(f"   来源工具: {tool_name}")
    print(f"   总轮次: {len(turns)}")
    print(f"   总字符: {total_chars:,}")
    print(f"   文件大小: {os.path.getsize(output_file):,} bytes")
    if args.user_only:
        print(f"   模式: 仅用户提问")


if __name__ == "__main__":
    main()
