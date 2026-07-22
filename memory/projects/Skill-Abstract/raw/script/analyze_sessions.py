#!/usr/bin/env python3
"""
分析 AI 会话记录中的高频词、常见短语、主题聚类 —— 纯本地计算，不消耗 AI token。

用法：
  python3 analyze_sessions.py                     # 分析所有会话
  python3 analyze_sessions.py --top 50            # 显示前 50 个高频词
  python3 analyze_sessions.py --select            # 交互式选择要分析的会话
  python3 analyze_sessions.py --recent 14         # 仅分析最近 14 天的会话
  python3 analyze_sessions.py --recent 7 --top 30 # 最近 7 天，前 30 关键词
  python3 analyze_sessions.py -o report.md        # 输出 Markdown 报告到文件
"""
import json, os, sys, re, argparse
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import math

# ── 导入 extract_qa 的提取逻辑 ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
from extract_qa import (
    scan_all_sessions, extract_qa, get_cached_meta,
    is_skill_injection, get_text_parts
)

# ═══════════════════════════════════════════════════════════
#  中文分词
# ═══════════════════════════════════════════════════════════

try:
    import jieba
    import jieba.posseg as pseg
    JIEBA_OK = True
except ImportError:
    JIEBA_OK = False


# ═══════════════════════════════════════════════════════════
#  停用词
# ═══════════════════════════════════════════════════════════

CN_STOP = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
    '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
    '没有', '看', '好', '自己', '这', '他', '她', '它', '们', '那', '些',
    '这个', '那个', '哪个', '怎么', '什么', '为什么', '如何', '可以', '还是',
    '或者', '但', '但是', '而', '而且', '所以', '因为', '如果', '虽然',
    '已经', '正在', '将', '把', '被', '让', '给', '对', '从', '以', '之',
    '与', '及', '等', '其', '中', '后', '前', '时', '来', '去', '做',
    '能', '能够', '可能', '应该', '需要', '想', '知道', '觉得', '认为',
    '用', '使用', '通过', '进行', '实现', '处理', '问题', '方式', '方面',
    '部分', '情况', '时候', '地方', '东西', '方法', '里面', '外面',
    '之后', '之前', '以后', '然后', '接着', '首先', '最后', '目前',
    '现在', '今天', '昨天', '明天', '一下', '一些', '一点', '很多',
    '比较', '非常', '特别', '更', '最', '很', '太', '真', '只', '还',
    '又', '再', '才', '刚', '已经', '曾经', '立即', '马上', '经常',
    '一直', '总是', '每次', '所有', '整个', '全部', '任何', '其他',
    '另外', '另', '该', '本', '此', '这样', '那样', '怎样', '这么',
    '那么', '哪', '哈', '啊', '吧', '呢', '吗', '哦', '嗯', '呀',
    '哎', '喂', '嗨', '嘿', '哇', '啦', '哟', '嘛',
    # 技术文档常见停用词
    '根据', '需要', '注意', '确保', '检查', '确认', '提供', '支持',
    '包含', '包括', '涉及', '相关', '对应', '具体', '一般', '基本',
    '主要', '重要', '简单', '复杂', '容易', '困难', '方便',
    '内容', '当前', '任务', '相关',
}

# 代码/系统注入噪音词（高频技术噪音，非用户真实话题）
CODE_NOISE = {
    # 系统提示注入
    'related', 'current', 'task', 'selected', 'lines',
    # C# / .NET 常用关键字
    'var', 'public', 'private', 'async', 'await', 'string', 'int', 'bool',
    'void', 'class', 'static', 'return', 'null', 'true', 'false', 'new',
    'foreach', 'object', 'namespace', 'using', 'typeof', 'get', 'set',
    # 构建配置
    'debug', 'release', 'any', 'cpu', 'activecfg', 'netcore',
    # 堆栈跟踪
    'system', 'threading', 'runtime', 'compilerservices', 'diagnostics',
    'reflection', 'linq', 'collections', 'asynctaskmethodbuilder', 'movenext',
    # 具体代码实体（项目特有噪音）
    'haton', 'hatoff', 'helmeteventtype', 'helmetid', 'personid', 'recordedat',
    'attendancerecord', 'attendancerecords', 'attendancerecordservice',
    'attendanceentity', 'attendanceruleentity', 'attendancesummaryservice',
    'workerid', 'workercontroller', 'workeronlineperiodqueryservice',
    'workdays', 'projectid', 'departmentid', 'requireddays',
    'defaultprojectservice', 'modulecode', 'modulerunner',
    # 随机 token 碎片（API key / JWT / hash 片段）
    'mawk', 'kuc', 'xv', 'pbjuvxw7tdfgcup5mzdllcrpgmnm',
    'prc5abmporlapjsee42poyzrti', 'm3jx4heu1lwawtyhguukqij',
    # 代码实体噪音
    'writeline', 'helmetids', 'startdate', 'enddate', 'datetimeoffset',
    'gridpolygons', 'f78c9d2', 'a361', 'x64', 'x86', 'build',
    # 过于通用的英文词（在技术语境中无区分度）
    'date', 'count', 'name', 'type', 'id', 'value', 'key', 'index',
    'item', 'data', 'info', 'result', 'list', 'file', 'files', 'path',
    # 系统消息/Cron/通知相关噪音
    'notification', 'fires', 'stops', 'live', 'background', 'children',
    'resume', 'notify', 'callback', 'contextcallback', 'send', 'another',
    'finished', 'accept', 'text', 'plain', 'microsoft', 'extensions',
    'message', 'event',
    # 过于通用的代码实体/参数
    'page', 'pagesize', 'pages', 'dal', 'datacenter', 'setresult',
    'masstransit', 'core', 'loc', 'locations', 'segmentstart',
    'validlocations', 'helmeteventtypes',
    # C# / 堆栈跟踪碎片
    'temp', 'readonly', 'box', 'boolean', 'call', 'completed',
    'runinternal', 'line', 'content', 'kestrel', 'aspnetcore',
    'hatevents', 'segments', 'tolist', 'hl',
}

EN_STOP = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'shall', 'need', 'must', 'to', 'of',
    'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'between', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'just', 'because', 'but', 'and', 'or', 'if',
    'while', 'about', 'up', 'out', 'off', 'over', 'down', 'also', 'now',
    'this', 'that', 'these', 'those', 'it', 'its', 'he', 'she', 'they',
    'them', 'we', 'you', 'me', 'us', 'him', 'her', 'his', 'my', 'your',
    'our', 'their', 'i', 'what', 'which', 'who', 'whom', 'get', 'got',
    'use', 'used', 'using', 'make', 'made', 'see', 'like', 'one', 'two',
    'way', 'new', 'also', 'well', 'back', 'end', 'put', 'set', 'let',
    'go', 'come', 'take', 'know', 'think', 'want', 'look', 'really',
    'still', 'thing', 'going', 'done', 'much', 'many', 'lot', 'even',
}


# ═══════════════════════════════════════════════════════════
#  文本清洗
# ═══════════════════════════════════════════════════════════

def clean_text(text):
    """清洗文本：去 XML、去路径、去代码块、去 URL"""
    # 去 XML 标签
    text = re.sub(r'<[^>]+>', ' ', text)
    # 去代码块
    text = re.sub(r'```[^`]*```', ' ', text)
    text = re.sub(r'`[^`]+`', ' ', text)
    # 去 URL
    text = re.sub(r'https?://\S+', ' ', text)
    # 去文件路径
    text = re.sub(r'/[\w/.-]+\.\w{1,8}', ' ', text)
    # 去系统提示文本
    text = re.sub(r'Caveat:.*?\.(?=\s|$)', '', text)
    text = re.sub(r'DO NOT respond.*?\.(?=\s|$)', '', text)
    text = re.sub(r'The user (opened|selected).*?\.(?=\s|$)', '', text)
    # 去纯数字/时间戳
    text = re.sub(r'\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}\S*', ' ', text)
    # 保留中英文、数字、下划线、连字符
    # (不替换，留到分词时处理)
    return text.strip()


def extract_text_from_md(filepath):
    """
    从 Markdown 文件中提取纯文本。
    自动处理 YAML frontmatter、代码块、链接、图片等。
    返回清洗后的文本字符串。
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 去 YAML frontmatter (--- ... ---)
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # 2. 去代码块
    content = re.sub(r'```[^`]*```', ' ', content, flags=re.DOTALL)

    # 3. 去行内代码
    content = re.sub(r'`[^`]+`', ' ', content)

    # 4. 去图片 ![alt](url)
    content = re.sub(r'!\[.*?\]\(.*?\)', ' ', content)

    # 5. 链接 [text](url) → 保留 text
    content = re.sub(r'\[([^\]]*?)\]\(.*?\)', r'\1', content)

    # 6. 去 HTML 标签
    content = re.sub(r'<[^>]+>', ' ', content)

    # 7. 去 Markdown 格式标记（粗体、斜体、列表符号）
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'\*(.*?)\*', r'\1', content)
    content = re.sub(r'^[-*+]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

    # 8. 去水平分割线
    content = re.sub(r'^[-*_]{3,}\s*$', '', content, flags=re.MULTILINE)

    # 9. 去 URL
    content = re.sub(r'https?://\S+', ' ', content)

    # 10. 去表格（保留为纯文本——表格行去掉 | 和 --- 分隔符）
    content = re.sub(r'\|', ' ', content)
    content = re.sub(r'^[\s-]{3,}\s*$', '', content, flags=re.MULTILINE)

    # 11. 合并空白
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)

    # 12. 拆分段落，过滤太短的
    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 15]

    result = ' '.join(paragraphs)

    # 最后过一遍通用清洗
    result = clean_text(result)

    return result


def analyze_file(filepath, args):
    """
    分析单个 Markdown 文件。
    返回 (all_tokens, session_tokens, session_texts, session_topics)
    与 build_corpus 输出格式兼容。
    """
    text = extract_text_from_md(filepath)
    if not text or len(text) < 50:
        print("❌ 文件内容不足（少于 50 字符有效文本）")
        return None, None, None, None

    tokens = tokenize(text)
    if not tokens:
        print("❌ 未能提取到有效词汇")
        return None, None, None, None

    # 按标题或段落切分为多个"伪会话"，用于聚类分析
    # 简单方案：按 \n\n 分段，每段作为独立单元
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
    if len(paragraphs) < 2:
        paragraphs = [text]  # 只有一段就用全文

    session_tokens_list = []
    session_texts_list = []

    for para in paragraphs:
        para_tokens = tokenize(para)
        if para_tokens and len(para_tokens) >= 5:
            session_tokens_list.append(('file', filepath, para_tokens))
            session_texts_list.append(('file', filepath, [para]))

    if not session_tokens_list:
        # fallback: 全文作为一个会话
        session_tokens_list = [('file', filepath, tokens)]
        session_texts_list = [('file', filepath, [text])]

    return tokens, session_tokens_list, session_texts_list


def is_noise_token(word):
    """过滤噪音 token：Markdown 标记、代码片段、堆栈跟踪、随机 ID"""
    # 纯标点 / 符号
    if re.match(r'^[#*=\-─━│┃⬤●○◉◦✓✔✗✘⬆⬇↑↓→←&|<>!~@%^+\\/:;,.`\'"\(\)\[\]\{\}]+$', word):
        return True
    # 堆栈跟踪模式: namespace.class.method 链
    if word.count('.') >= 2 and any(c.isalpha() for c in word):
        return True
    # .NET 堆栈跟踪前缀
    if re.match(r'^system\.(runtime|threading|compilerservices|diagnostics|reflection|linq|collections|text|io|net|web|data)', word):
        return True
    # 驼峰链: WordAnotherWordSomething (3+ 大写字母)
    if re.match(r'^[a-z]+[A-Z][a-z]+[A-Z][a-z]+[A-Z]', word):
        return True
    # 过长的随机字符串（base64 / UUID / token）
    if len(word) > 20 and re.match(r'^[a-zA-Z0-9+/=_-]+$', word):
        return True
    # 全辅音或无元音的长串（随机 ID）
    if len(word) > 8 and re.match(r'^[bcdfghjklmnpqrstvwxyz]{4,}$', word, re.IGNORECASE):
        return True
    # GUID / UUID 模式
    if re.match(r'^[a-f0-9]{8,}-[a-f0-9-]+$', word):
        return True
    # 纯数字
    if re.match(r'^[0-9]+$', word):
        return True
    # 纯下划线/点号链
    if re.match(r'^[_.]+$', word):
        return True
    # 连续小写复合词（threadpoolthread, continuationobject 等堆栈碎片）
    if len(word) > 12 and re.match(r'^[a-z]{12,}$', word):
        return True
    # Hash 碎片：纯 hex 字符 [a-f0-9]
    # ≥8 位 → 几乎一定是 hash（SHA 片段）
    if re.match(r'^[a-f0-9]{8,}$', word):
        return True
    # 3-7 位且含数字 → hash 片段（ead 等 3 字母真实单词放行）
    if re.match(r'^[a-f0-9]{3,7}$', word) and re.search(r'[0-9]', word):
        return True
    return False


def is_noise_phrase(phrase):
    """短语级噪音过滤：代码碎片、纯系统消息、无实质内容"""
    parts = phrase.split()
    # 所有词都在 CODE_NOISE 中 → 噪音
    if all(p in CODE_NOISE for p in parts):
        return True
    # 大部分词是噪音 token
    noise_count = sum(1 for p in parts if is_noise_token(p))
    if noise_count > len(parts) * 0.5:
        return True
    # 短语看起来像代码行后缀（XxxThread, XxxCallback, XxxHandler...）
    phrase_str = ' '.join(parts)
    code_suffixes = r'(thread|callback|handler|builder|factory|provider|manager|service|controller|repository|token|notification|message|event|context|object)$'
    if re.match(rf'^[a-z]+\s+[a-z]+{code_suffixes}', phrase_str):
        return True
    return False


# ═══════════════════════════════════════════════════════════
#  分词
# ═══════════════════════════════════════════════════════════

def tokenize(text):
    """
    对中英混合文本分词，返回单词列表。
    中文用 jieba 分词 + 词性过滤；英文按空格/标点切分。
    """
    tokens = []

    if JIEBA_OK:
        # 用 jieba 分词 + 词性标注
        words = pseg.cut(text)
        for word, flag in words:
            word = word.strip().lower()
            if not word or len(word) < 2:
                continue
            # 过滤停用词 + 代码噪音
            if word in CN_STOP or word in EN_STOP or word in CODE_NOISE:
                continue
            # 过滤噪音 token
            if is_noise_token(word):
                continue
            # 词性过滤：保留名词、动词、英文、未知
            keep_flags = {'n', 'v', 'eng', 'x', 'nr', 'ns', 'nt', 'nz',
                          'vn', 'an', 'j', 'l', 'i'}
            if flag in keep_flags or flag.startswith('n') or flag.startswith('v'):
                tokens.append(word)
    else:
        # Fallback: 简单的中英混合分词
        for match in re.finditer(r'[一-鿿]{2,}|[a-zA-Z][a-zA-Z0-9_./-]*[a-zA-Z0-9]|[a-zA-Z]{2,}', text):
            word = match.group().lower()
            if word not in CN_STOP and word not in EN_STOP and word not in CODE_NOISE and len(word) >= 2:
                if not is_noise_token(word):
                    tokens.append(word)

    return tokens


def extract_bigrams(tokens):
    """从 token 序列中提取 bigram"""
    return [' '.join(tokens[i:i + 2]) for i in range(len(tokens) - 1)]


def extract_trigrams(tokens):
    """从 token 序列中提取 trigram"""
    return [' '.join(tokens[i:i + 3]) for i in range(len(tokens) - 2)]


def is_meaningful_phrase(phrase):
    """过滤掉纯停用词、代码噪音、纯标点、或同一词重复的短语"""
    parts = phrase.split()
    if len(parts) < 2:
        return False
    # 同一 token 连续重复（如 "last30days last30days"）
    if len(set(parts)) == 1:
        return False
    meaningful = sum(1 for p in parts
                     if p not in CN_STOP and p not in EN_STOP and p not in CODE_NOISE
                     and not is_noise_token(p))
    return meaningful >= len(parts) * 0.5


# ── POS 模式定义（好搭配的词性组合） ──

# 中文好模式：两个有实质内容的词相邻
GOOD_POS_PATTERNS_2 = {
    ('n', 'n'), ('n', 'v'), ('v', 'n'), ('a', 'n'), ('n', 'a'),
    ('vn', 'n'), ('n', 'vn'), ('an', 'n'), ('n', 'an'),
    ('v', 'v'), ('vn', 'v'), ('v', 'vn'),
    ('ns', 'n'), ('n', 'ns'), ('nr', 'n'), ('n', 'nr'),
    ('eng', 'n'), ('n', 'eng'), ('eng', 'v'), ('v', 'eng'),
    ('eng', 'eng'), ('eng', 'a'), ('a', 'eng'),
    ('nz', 'n'), ('n', 'nz'), ('j', 'n'), ('n', 'j'),
    # 允许一个虚词在中间（如"API 的 调用"→ 已过滤，这里不做）
}

# 坏 POS 模式：两个虚词/代词/标点相邻 → 降权
BAD_POS_PATTERNS_2 = {
    ('uj', 'n'), ('n', 'uj'), ('ul', 'v'), ('v', 'ul'),
    ('p', 'n'), ('n', 'p'), ('p', 'v'), ('v', 'p'),
    ('r', 'n'), ('n', 'r'), ('r', 'v'), ('v', 'r'),
    ('d', 'n'), ('n', 'd'), ('d', 'v'), ('v', 'd'),
    ('m', 'n'), ('q', 'n'), ('m', 'v'),
    ('c', 'n'), ('n', 'c'), ('c', 'v'), ('v', 'c'),
    ('x', 'n'), ('n', 'x'), ('x', 'x'),
}


def score_phrase_pos(phrase):
    """
    用 jieba POS 对短语做词性模式评分。
    返回 1.0（完美名动搭配）~ 0.0（纯虚词噪音）
    """
    if not JIEBA_OK:
        return 0.5  # 没有 jieba 时中性评分

    words = list(pseg.cut(phrase))
    poses = [w.flag for w in words if w.flag not in ('x', 'w', 'm', 'q')]

    if len(poses) < 2:
        return 0.3

    if len(poses) == 2:
        if tuple(poses) in GOOD_POS_PATTERNS_2:
            return 1.0
        if tuple(poses) in BAD_POS_PATTERNS_2:
            return 0.1
        # 任意 n-开头的词 + n-开头的词
        if poses[0].startswith('n') and poses[1].startswith('n'):
            return 0.85
        if poses[0].startswith('v') and poses[1].startswith('n'):
            return 0.85
        if poses[0].startswith('n') and poses[1].startswith('v'):
            return 0.8
        return 0.35

    else:
        # trigram: 滑动窗口取平均
        scores = []
        for i in range(len(poses) - 1):
            pair = (poses[i], poses[i + 1])
            if pair in GOOD_POS_PATTERNS_2:
                scores.append(1.0)
            elif pair in BAD_POS_PATTERNS_2:
                scores.append(0.1)
            elif pair[0].startswith('n') and pair[1].startswith('n'):
                scores.append(0.8)
            elif pair[0].startswith('v') and pair[1].startswith('n'):
                scores.append(0.8)
            else:
                scores.append(0.3)
        return sum(scores) / len(scores) if scores else 0.3


def analyze_phrases_pmi(all_tokens, top_n=20, min_freq=3):
    """
    基于 PMI + POS 模式 + 频率的综合短语评分。

    PMI(w1,w2) = log(P(w1,w2) / (P(w1) * P(w2)))
    高 PMI → 两个词"真正绑在一起"，而非偶然相邻。

    Combined = PMI × log(freq) × POS_bonus
    """
    word_counts = Counter(all_tokens)
    N_words = len(all_tokens)

    # ── Bigram PMI ──
    bigrams_raw = extract_bigrams(all_tokens)
    bigram_counter = Counter(
        b for b in bigrams_raw
        if is_meaningful_phrase(b) and not is_noise_phrase(b)
    )
    total_bigrams = sum(bigram_counter.values())

    scored_bigrams = []
    for phrase, freq in bigram_counter.items():
        if freq < min_freq:
            continue
        parts = phrase.split()
        if len(parts) != 2:
            continue

        # PMI
        p_w1 = word_counts.get(parts[0], 1) / N_words
        p_w2 = word_counts.get(parts[1], 1) / N_words
        p_joint = freq / max(total_bigrams, 1)
        if p_w1 > 0 and p_w2 > 0 and p_joint > 0:
            pmi = math.log(p_joint / (p_w1 * p_w2))
        else:
            pmi = 0.0

        # POS 加成
        pos_score = score_phrase_pos(phrase)

        # 综合分（至少保留基础分）
        combined = max(0.01, pmi) * math.log(freq + 1) * (0.25 + 0.75 * pos_score)

        scored_bigrams.append((phrase, freq, round(pmi, 2), round(combined, 3)))

    scored_bigrams.sort(key=lambda x: x[3], reverse=True)

    # ── Trigram（用平均 pairwise PMI + POS）──
    trigrams_raw = extract_trigrams(all_tokens)
    trigram_counter = Counter(
        t for t in trigrams_raw
        if is_meaningful_phrase(t) and not is_noise_phrase(t)
    )
    total_trigrams = sum(trigram_counter.values())

    scored_trigrams = []
    for phrase, freq in trigram_counter.items():
        if freq < min_freq:
            continue
        parts = phrase.split()
        if len(parts) != 3:
            continue

        # 平均 pairwise PMI
        pmi_sum = 0.0
        pairs_ok = 0
        for i in range(2):
            w_a, w_b = parts[i], parts[i + 1]
            p_wa = word_counts.get(w_a, 1) / N_words
            p_wb = word_counts.get(w_b, 1) / N_words
            # 用 bigram 计数估算 joint
            pair_str = f'{w_a} {w_b}'
            pair_freq = bigram_counter.get(pair_str, 1)
            p_joint = pair_freq / max(total_bigrams, 1)
            if p_wa > 0 and p_wb > 0 and p_joint > 0:
                pmi_sum += math.log(p_joint / (p_wa * p_wb))
                pairs_ok += 1

        avg_pmi = pmi_sum / max(pairs_ok, 1)

        pos_score = score_phrase_pos(phrase)
        combined = max(0.01, avg_pmi) * math.log(freq + 1) * (0.25 + 0.75 * pos_score)

        scored_trigrams.append((phrase, freq, round(avg_pmi, 2), round(combined, 3)))

    scored_trigrams.sort(key=lambda x: x[3], reverse=True)

    return scored_bigrams[:top_n], scored_trigrams[:top_n]


# 兼容旧接口
def analyze_phrases(all_tokens, top_n=20):
    """兼容旧调用，内部使用 PMI"""
    bis, tris = analyze_phrases_pmi(all_tokens, top_n=top_n, min_freq=2)
    # 返回 (phrase, count) 格式兼容旧代码
    return [(p, f) for p, f, _, _ in bis], [(p, f) for p, f, _, _ in tris]


# ═══════════════════════════════════════════════════════════
#  会话内容提取
# ═══════════════════════════════════════════════════════════

def extract_user_questions(session_file):
    """从会话文件中提取所有用户提问文本（清洗后）"""
    texts = []
    try:
        turns = extract_qa(session_file)
        for t in turns:
            cleaned = clean_text(t['user'])
            if cleaned and len(cleaned) > 10:
                texts.append(cleaned)
    except Exception:
        pass
    return texts


def build_corpus(sessions):
    """
    从会话列表构建语料库。
    返回:
      all_tokens: 全局 token 列表
      session_tokens: [(tool, path, tokens_list), ...]
      session_texts: [(tool, path, [text, ...]), ...]
    """
    all_tokens = []
    session_tokens = []
    session_texts = []

    for tool, path, _mtime, _size in sessions:
        texts = extract_user_questions(path)
        if not texts:
            continue

        session_texts.append((tool, path, texts))

        tokens = []
        for text in texts:
            toks = tokenize(text)
            tokens.extend(toks)
            all_tokens.extend(toks)

        if tokens:
            session_tokens.append((tool, path, tokens))

    return all_tokens, session_tokens, session_texts


# ═══════════════════════════════════════════════════════════
#  分析函数
# ═══════════════════════════════════════════════════════════

def analyze_word_freq(all_tokens, top_n=30):
    """词频分析：返回 [(word, count), ...]"""
    counter = Counter(all_tokens)
    # 过滤太短的词
    filtered = [(w, c) for w, c in counter.items() if len(w) >= 2]
    return filtered[:top_n]


def analyze_phrases(all_tokens, top_n=20):
    """提取高频 bigram 和 trigram"""
    bigrams = extract_bigrams(all_tokens)
    trigrams = extract_trigrams(all_tokens)

    bi_counter = Counter(b for b in bigrams if is_meaningful_phrase(b))
    tri_counter = Counter(t for t in trigrams if is_meaningful_phrase(t))

    return bi_counter.most_common(top_n), tri_counter.most_common(top_n)


def analyze_session_topics(session_tokens, top_per_session=8):
    """每个会话的高频词"""
    results = []
    for tool, path, tokens in session_tokens:
        counter = Counter(tokens)
        meta = get_cached_meta(path)
        results.append({
            'path': path,
            'tool': tool,
            'title': meta.get('title', ''),
            'start_ts': meta.get('start_ts'),
            'end_ts': meta.get('end_ts'),
            'keywords': counter.most_common(top_per_session),
            'total_tokens': len(tokens),
        })
    return results


def cluster_sessions(session_tokens, min_shared=2):
    """
    简单主题聚类：基于共享关键词对会话分组。
    返回 clusters: [[session_index, ...], ...]
    """
    n = len(session_tokens)
    if n <= 1:
        return [list(range(n))]

    # 为每个会话提取 top-10 关键词集合
    session_keywords = []
    for _, _, tokens in session_tokens:
        top_words = set(w for w, _ in Counter(tokens).most_common(10))
        session_keywords.append(top_words)

    # 构建邻接矩阵：共享 ≥ min_shared 个关键词 → 边
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            shared = session_keywords[i] & session_keywords[j]
            if len(shared) >= min_shared:
                adj[i].add(j)
                adj[j].add(i)

    # BFS 找连通分量
    visited = set()
    clusters = []
    for i in range(n):
        if i in visited:
            continue
        component = []
        queue = [i]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            component.append(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
        clusters.append(component)

    # 没参与任何聚类的单独成组
    for i in range(n):
        if i not in visited:
            clusters.append([i])

    clusters.sort(key=len, reverse=True)
    return clusters


def cluster_label(cluster, session_topics, max_words=5):
    """为一个聚类的会话生成描述标签（取组内最共有的关键词）"""
    all_keywords = Counter()
    for idx in cluster:
        for w, c in session_topics[idx]['keywords']:
            all_keywords[w] += c

    # 在 >= 2 个会话中出现的关键词优先
    shared = []
    unshared = []
    for w, c in all_keywords.most_common(20):
        count_in_sessions = sum(
            1 for idx in cluster
            if w in dict(session_topics[idx]['keywords'])
        )
        if count_in_sessions >= 2:
            shared.append(w)
        else:
            unshared.append(w)

    label_words = (shared + unshared)[:max_words]
    return ', '.join(label_words)


def analyze_trends(session_topics, recent_days=7):
    """
    对比近期 vs 更早的关键词趋势。
    返回 (rising, falling) 各为 [(word, score), ...]
    """
    now = datetime.now().timestamp()
    cutoff = now - recent_days * 86400

    recent_counter = Counter()
    older_counter = Counter()

    for s in session_topics:
        ts = s.get('start_ts')
        if ts is None:
            continue
        for w, c in s['keywords']:
            if ts >= cutoff:
                recent_counter[w] += c
            else:
                older_counter[w] += c

    # 计算 TF 比率（加平滑）
    total_recent = sum(recent_counter.values()) or 1
    total_older = sum(older_counter.values()) or 1

    trends = []
    all_words = set(recent_counter.keys()) | set(older_counter.keys())
    for w in all_words:
        freq_recent = recent_counter[w] / total_recent
        freq_older = older_counter[w] / total_older
        if freq_recent + freq_older < 0.001:  # 过滤极低频
            continue
        ratio = (freq_recent + 0.0001) / (freq_older + 0.0001)
        trends.append((w, ratio, recent_counter[w], older_counter[w]))

    trends.sort(key=lambda x: x[1], reverse=True)
    rising = [(w, r, rc, oc) for w, r, rc, oc in trends if r > 1.5 and rc >= 2][:15]
    falling = [(w, r, rc, oc) for w, r, rc, oc in trends if r < 0.67 and oc >= 2][:15]
    falling.reverse()  # 最显著下降排前面

    return rising, falling


# ═══════════════════════════════════════════════════════════
#  输出
# ═══════════════════════════════════════════════════════════

def format_bar(count, max_count, width=12):
    """简易 ASCII 条状图"""
    if max_count == 0:
        return ''
    bar_len = int(count / max_count * width)
    return '█' * bar_len


def print_header(title):
    print()
    print('─' * 70)
    print(f'  {title}')
    print('─' * 70)


def format_ts(ts):
    if ts is None:
        return '?'
    return datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")


def print_report(args, all_tokens, session_tokens, session_texts, session_topics):
    """终端输出分析报告"""
    sessions_total = len(session_texts)
    total_questions = sum(len(texts) for _, _, texts in session_texts)
    total_chars = sum(
        sum(len(t) for t in texts) for _, _, texts in session_texts
    )
    unique_words = len(set(all_tokens))

    # ── 头部 ──
    print()
    print('╔' + '═' * 68 + '╗')
    print('║  🧠 AI 会话分析报告' + ' ' * 48 + '║')
    print('╠' + '═' * 68 + '╣')
    print(f'║  会话数: {sessions_total:<6}  |  提问轮次: {total_questions:<6}  |  总字数: {total_chars:>8,}  ║')
    print(f'║  独特词数: {unique_words:<6}  |  总词频: {len(all_tokens):>8,}                        ║')
    print('╚' + '═' * 68 + '╝')

    # ── 高频关键词 ──
    word_freq = analyze_word_freq(all_tokens, top_n=args.top)
    max_count = word_freq[0][1] if word_freq else 1

    print_header(f'🔥 高频关键词 (Top {args.top})')
    print(f'{"关键词":<20} {"频次":>6}  {"分布"}')
    print('─' * 70)
    for w, c in word_freq[:args.top]:
        bar = format_bar(c, max_count)
        print(f'{w:<20} {c:>6}  {bar}')

    # ── 常见短语（PMI 评分） ──
    bigrams, trigrams = analyze_phrases_pmi(
        all_tokens, top_n=args.top // 2, min_freq=args.min_phrase_freq
    )
    print_header(f'📝 常见短语（PMI 评分：越高越"真正绑定"）')
    if bigrams:
        print(f'  {"2-gram":<35} {"频次":>5}  {"PMI":>6}  {"综合":>6}')
        print('  ' + '─' * 58)
        for phrase, freq, pmi, combined in bigrams[:args.top // 2]:
            print(f'  {phrase:<35} {freq:>5}  {pmi:>6.2f}  {combined:>6.3f}')
    if trigrams:
        print(f'\n  {"3-gram":<35} {"频次":>5}  {"PMI":>6}  {"综合":>6}')
        print('  ' + '─' * 58)
        for phrase, freq, pmi, combined in trigrams[:args.top // 3]:
            print(f'  {phrase:<35} {freq:>5}  {pmi:>6.2f}  {combined:>6.3f}')

    # ── 主题聚类 ──
    clusters = cluster_sessions(session_tokens, min_shared=2)
    print_header(f'📂 主题聚类 ({len(clusters)} 组)')

    for ci, cluster in enumerate(clusters):
        if len(cluster) < 2 and ci > 10:
            # 单会话组太多，合并显示
            remaining = sum(1 for c in clusters[ci:] if len(c) == 1)
            if remaining > 0:
                print(f'  … 其余 {remaining} 个独立主题会话')
            break

        label = cluster_label(cluster, session_topics)
        session_list = ', '.join(
            f"#{cluster[si]}"
            for si in range(min(3, len(cluster)))
        )
        if len(cluster) > 3:
            session_list += f' …共 {len(cluster)} 个'

        print(f'  🏷️  [{label}]')
        print(f'      {session_list}')
        print()

    # ── 近期趋势 ──
    if args.recent > 0:
        rising, falling = analyze_trends(session_topics, recent_days=args.recent)
        print_header(f'📈 趋势对比 (最近 {args.recent} 天 vs 更早)')

        if rising:
            print('  🔺 上升:')
            for w, ratio, rc, oc in rising[:10]:
                print(f'      {w:<25} 最近×{rc}  更早×{oc}')
        if falling:
            print('  🔻 下降:')
            for w, ratio, rc, oc in falling[:10]:
                print(f'      {w:<25} 最近×{rc}  更早×{oc}')
        if not rising and not falling:
            print('  （数据不足以分析趋势）')

    # ── 会话摘要 ──
    if args.verbose:
        print_header(f'📋 会话摘要 (Top {min(5, args.top)} 关键词/会话)')
        for i, s in enumerate(session_topics):
            keywords_str = ', '.join(
                f'{w}({c})' for w, c in s['keywords'][:5]
            )
            title = s['title'][:50] if s['title'] else '(无标题)'
            print(f'  #{i + 1:<4} {keywords_str}')
            print(f'         {title}')
            print()

    print()
    print('─' * 70)
    print('  💡 提示: 使用 -o report.md 保存完整报告')
    print('─' * 70)
    print()


def write_markdown_report(
    out_file, args, all_tokens, session_tokens, session_texts, session_topics
):
    """输出完整 Markdown 报告"""
    sessions_total = len(session_texts)
    total_questions = sum(len(texts) for _, _, texts in session_texts)
    total_chars = sum(sum(len(t) for t in texts) for _, _, texts in session_texts)
    unique_words = len(set(all_tokens))
    word_freq = analyze_word_freq(all_tokens, top_n=args.top)
    bigrams, trigrams = analyze_phrases_pmi(
        all_tokens, top_n=args.top // 2, min_freq=args.min_phrase_freq
    )
    clusters = cluster_sessions(session_tokens, min_shared=2)

    with open(out_file, 'w') as f:
        f.write(f'# 🧠 AI 会话分析报告\n\n')
        f.write(f'**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n')
        f.write(f'## 📊 总览\n\n')
        f.write(f'| 指标 | 数值 |\n')
        f.write(f'|------|------|\n')
        f.write(f'| 会话数 | {sessions_total} |\n')
        f.write(f'| 提问轮次 | {total_questions} |\n')
        f.write(f'| 总字数 | {total_chars:,} |\n')
        f.write(f'| 独特词数 | {unique_words} |\n')
        f.write(f'| 总词频 | {len(all_tokens):,} |\n')
        f.write(f'\n')

        f.write(f'## 🔥 高频关键词 (Top {args.top})\n\n')
        f.write(f'| 关键词 | 频次 |\n')
        f.write(f'|--------|------|\n')
        for w, c in word_freq[:args.top]:
            f.write(f'| {w} | {c} |\n')
        f.write(f'\n')

        f.write(f'## 📝 常见短语（PMI 评分）\n\n')
        if bigrams:
            f.write(f'### 2-gram\n\n')
            f.write(f'| 短语 | 频次 | PMI | 综合分 |\n')
            f.write(f'|------|------|-----|--------|\n')
            for phrase, freq, pmi, combined in bigrams[:args.top // 2]:
                f.write(f'| {phrase} | {freq} | {pmi} | {combined} |\n')
            f.write(f'\n')
        if trigrams:
            f.write(f'### 3-gram\n\n')
            f.write(f'| 短语 | 频次 | PMI | 综合分 |\n')
            f.write(f'|------|------|-----|--------|\n')
            for phrase, freq, pmi, combined in trigrams[:args.top // 3]:
                f.write(f'| {phrase} | {freq} | {pmi} | {combined} |\n')
            f.write(f'\n')

        f.write(f'## 📂 主题聚类 ({len(clusters)} 组)\n\n')
        for ci, cluster in enumerate(clusters):
            if len(cluster) < 2:
                continue
            label = cluster_label(cluster, session_topics)
            f.write(f'### 组 {ci + 1}: {label}\n\n')
            f.write(f'| # | 会话标题 | 关键词 |\n')
            f.write(f'|---|----------|--------|\n')
            for idx in cluster:
                s = session_topics[idx]
                title = s['title'][:60] if s['title'] else '(无标题)'
                kw = ', '.join(w for w, _ in s['keywords'][:6])
                f.write(f'| {idx + 1} | {title} | {kw} |\n')
            f.write(f'\n')

        if args.recent > 0:
            rising, falling = analyze_trends(session_topics, recent_days=args.recent)
            f.write(f'## 📈 趋势对比 (最近 {args.recent} 天 vs 更早)\n\n')
            if rising:
                f.write(f'### 🔺 上升\n\n')
                f.write(f'| 关键词 | 最近频次 | 更早频次 |\n')
                f.write(f'|--------|----------|----------|\n')
                for w, ratio, rc, oc in rising[:15]:
                    f.write(f'| {w} | {rc} | {oc} |\n')
                f.write(f'\n')
            if falling:
                f.write(f'### 🔻 下降\n\n')
                f.write(f'| 关键词 | 最近频次 | 更早频次 |\n')
                f.write(f'|--------|----------|----------|\n')
                for w, ratio, rc, oc in falling[:15]:
                    f.write(f'| {w} | {rc} | {oc} |\n')
                f.write(f'\n')

        f.write(f'## 📋 全部会话摘要\n\n')
        f.write(f'| # | 时间 | 标题 | Top 关键词 |\n')
        f.write(f'|---|------|------|------------|\n')
        for i, s in enumerate(session_topics):
            ts = format_ts(s.get('start_ts'))
            title = s['title'][:50] if s['title'] else '(无标题)'
            kw = ', '.join(f'{w}({c})' for w, c in s['keywords'][:5])
            f.write(f'| {i + 1} | {ts} | {title} | {kw} |\n')


# ═══════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════

def parse_range(input_str, max_idx):
    """解析 "1,3,5-8" 或 "all" → 0-based 索引列表"""
    s = input_str.strip()
    if s.lower() in ('all', 'a'):
        return list(range(max_idx))
    selected = set()
    for part in re.split(r'[,，\s]+', s):
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
                pass
        else:
            try:
                i = int(part)
                if 1 <= i <= max_idx:
                    selected.add(i - 1)
            except ValueError:
                pass
    return sorted(selected)


def main():
    parser = argparse.ArgumentParser(description='分析 AI 编码工具会话记录（纯本地计算）')
    parser.add_argument('--top', type=int, default=30, help='显示前 N 个高频词（默认 30）')
    parser.add_argument('--select', action='store_true', help='交互式选择要分析的会话')
    parser.add_argument('--recent', type=int, default=0,
                        help='仅分析最近 N 天的会话（0=全部，同时启用趋势对比）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示每个会话的关键词摘要')
    parser.add_argument('--min-pmi', type=float, default=0.5,
                        help='短语最低 PMI 阈值（默认 0.5，越高越严格）')
    parser.add_argument('--min-phrase-freq', type=int, default=3,
                        help='短语最低出现次数（默认 3）')
    parser.add_argument('-o', '--output', help='保存 Markdown 报告到文件')
    parser.add_argument('--file', '-f', help='分析指定的 Markdown 文件（而非会话记录）')
    args = parser.parse_args()

    # ── --file 模式：分析单个 Markdown 文件 ──
    if args.file:
        filepath = os.path.expanduser(args.file)
        if not os.path.isfile(filepath):
            print(f"❌ 文件不存在: {filepath}")
            return

        print(f"\n⏳ 正在分析: {filepath}")
        all_tokens, session_tokens, session_texts = analyze_file(filepath, args)

        if not all_tokens:
            return

        session_topics = analyze_session_topics(session_tokens)
        word_freq = analyze_word_freq(all_tokens, top_n=args.top)
        bigrams, trigrams = analyze_phrases_pmi(
            all_tokens, top_n=args.top // 2, min_freq=args.min_phrase_freq
        )

        # 精简报告（无趋势、简化聚类）
        unique_words = len(set(all_tokens))
        total_paras = len(session_texts)

        print()
        print('╔' + '═' * 68 + '╗')
        print(f'║  📄 文档分析: {os.path.basename(filepath)[:50]}')
        print('╠' + '═' * 68 + '╣')
        print(f'║  段落数: {total_paras:<6}  |  总字数: {len(" ".join(str(t) for t in all_tokens)):>8,}  ║')
        print(f'║  独特词数: {unique_words:<6}  |  总词频: {len(all_tokens):>8,}                        ║')
        print('╚' + '═' * 68 + '╝')

        max_count = word_freq[0][1] if word_freq else 1
        print_header(f'🔥 高频关键词 (Top {args.top})')
        print(f'{"关键词":<20} {"频次":>6}  {"分布"}')
        print('─' * 70)
        for w, c in word_freq[:args.top]:
            bar = format_bar(c, max_count)
            print(f'{w:<20} {c:>6}  {bar}')

        print_header(f'📝 常见短语（PMI 评分）')
        if bigrams:
            print(f'  {"2-gram":<35} {"频次":>5}  {"PMI":>6}  {"综合":>6}')
            print('  ' + '─' * 58)
            for phrase, freq, pmi, combined in bigrams[:args.top // 2]:
                print(f'  {phrase:<35} {freq:>5}  {pmi:>6.2f}  {combined:>6.3f}')
        if trigrams:
            print(f'\n  {"3-gram":<35} {"频次":>5}  {"PMI":>6}  {"综合":>6}')
            print('  ' + '─' * 58)
            for phrase, freq, pmi, combined in trigrams[:args.top // 3]:
                print(f'  {phrase:<35} {freq:>5}  {pmi:>6.2f}  {combined:>6.3f}')

        # 聚类（段落间）
        if len(session_tokens) >= 2:
            clusters = cluster_sessions(session_tokens, min_shared=1)
            print_header(f'📂 段落聚类 ({len(clusters)} 组)')
            for ci, cluster in enumerate(clusters[:12]):
                label = cluster_label(cluster, session_topics)
                if len(cluster) >= 2:
                    print(f'  🏷️  [{label}] — {len(cluster)} 个段落')

        print()
        print('─' * 70)
        print('  💡 提示: 使用 -o report.md 保存完整报告')
        print('─' * 70)
        print()
        return

    # ── 获取会话列表 ──
    all_sessions = scan_all_sessions()
    if not all_sessions:
        print("未找到任何会话文件")
        return

    # ── 过滤：--recent ──
    if args.recent > 0:
        cutoff = (datetime.now() - timedelta(days=args.recent)).timestamp()
        all_sessions = [s for s in all_sessions if s[2] >= cutoff]
        if not all_sessions:
            print(f"最近 {args.recent} 天内没有会话")
            return

    # ── --select 交互式选择 ──
    if args.select:
        # 临时导入 list 功能
        from extract_qa import list_sessions, get_cached_meta as _gcm
        print()
        for idx, (tool, path, _mt, size) in enumerate(all_sessions):
            meta = get_cached_meta(path)
            ts = format_ts(meta.get('start_ts'))
            print(f'  #{idx + 1:<4} {ts}  {tool:<14}  {meta.get("title", "")[:55]}')

        print()
        print("输入要分析的会话编号，如: 1,3,5-8 或 all（直接回车取消）")
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已取消")
            return
        if not user_input:
            print("已取消")
            return

        indices = parse_range(user_input, len(all_sessions))
        if not indices:
            print("未选中任何会话")
            return
        all_sessions = [all_sessions[i] for i in indices]
        print(f"已选择 {len(all_sessions)} 个会话")

    print(f"\n⏳ 正在分析 {len(all_sessions)} 个会话…")

    # ── 构建语料库 ──
    all_tokens, session_tokens, session_texts = build_corpus(all_sessions)

    if not all_tokens:
        print("未提取到有效文本内容")
        return

    # ── 分析 ──
    session_topics = analyze_session_topics(session_tokens)

    # ── 输出 ──
    if args.output:
        out_file = os.path.expanduser(args.output)
        os.makedirs(os.path.dirname(out_file) or '.', exist_ok=True)
        write_markdown_report(
            out_file, args, all_tokens, session_tokens,
            session_texts, session_topics
        )
        print(f"✅ 报告已保存: {out_file}")

    print_report(args, all_tokens, session_tokens, session_texts, session_topics)


if __name__ == '__main__':
    main()
