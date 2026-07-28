#!/usr/bin/env python3
"""
convert_mindmap.py
~~~~~~~~~~~~~~~~~~
将 source/raw_mindmap/ 中的树形文本文件转换为 Hexo markmap 思维导图格式，
输出到 source/mindmap/source/。

支持的树形格式（使用 ├─ └─ │ 等 box-drawing 字符）：
    ├─ 【系统组成层・整体包含关系】
    │  └─ DBS 数据库系统（最大范畴）
    │     ├─ DB 数据库
    │     └─ DBMS 数据库管理系统

用法：
    python scripts/convert_mindmap.py                    # 转换所有新文件
    python scripts/convert_mindmap.py --force            # 强制重新转换所有文件
    python scripts/convert_mindmap.py --check            # 仅检查，列出待转换文件
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path

# 路径配置（相对于项目根目录）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "source" / "raw_mindmap"
OUTPUT_DIR = PROJECT_ROOT / "source" / "mindmap" / "source"
CACHE_FILE = PROJECT_ROOT / "source" / "mindmap" / ".convert_cache.json"

# 不需要转换的文件
SKIP_FILES = {".DS_Store", "README.md", ".gitkeep"}


def load_cache() -> dict:
    """加载转换缓存（记录已转换文件的 hash）。"""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def save_cache(cache: dict) -> None:
    """保存转换缓存。"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def file_hash(filepath: Path) -> str:
    """计算文件内容的 MD5 hash。"""
    return hashlib.md5(filepath.read_bytes()).hexdigest()


def parse_tree_line(line: str):
    """
    解析一行树形文本，返回 (depth, content) 或 (None, None)。

    树形字符识别：
      ├ └ ┌ ┐  → 节点标记（branch / last branch）
      │         → 垂直连接线
      ─         → 水平连接线

    深度计算：基于节点标记（├└）的列位置 ÷ 3。
    每一级缩进占约 3 个字符宽度（│ + 2空格）。
    """
    line = line.rstrip("\n\r")
    if not line.strip():
        return None, None

    # 找节点标记位置（├ 或 └）
    marker_pos = -1
    for i, ch in enumerate(line):
        if ch in ("├", "└", "┌", "┐"):
            marker_pos = i
            break

    # 没有节点标记的行（纯文本说明），作为 depth 0 处理
    if marker_pos < 0:
        content = line.strip()
        if content:
            return 0, content
        return None, None

    # 深度 = 标记位置 ÷ 3（每级树形缩进约占 3 个字符宽）
    depth = max(0, marker_pos // 3)

    # 提取内容：跳过标记字符（├─ 或 └─ 等）
    suffix = line[marker_pos:]
    content_start = 0
    tree_chars = set("├└─│┐┌ ")
    for ch in suffix:
        if ch in tree_chars:
            content_start += 1
        else:
            break
    content = suffix[content_start:].strip()

    if not content:
        return None, None

    return depth, content


def convert_tree_to_markmap(text: str) -> str:
    """
    将树形文本转换为 markmap 兼容的 markdown 列表格式。

    输入：
        ├─ 根节点
        │  ├─ 子节点1
        │  └─ 子节点2

    输出：
        - 根节点
          - 子节点1
          - 子节点2
    """
    lines = text.split("\n")
    parsed = []
    for line in lines:
        depth, content = parse_tree_line(line)
        if depth is not None and content:
            parsed.append((depth, content))

    if not parsed:
        return ""

    # 构建 markdown 列表
    result_lines = []
    for depth, content in parsed:
        indent = "  " * depth  # 每级缩进 2 个空格
        content_escaped = content.replace("<", "&lt;").replace(">", "&gt;")
        result_lines.append(f"{indent}- {content_escaped}")

    return "\n".join(result_lines)


def generate_frontmatter(title: str, date: str = None) -> str:
    """生成 Hexo frontmatter。"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""---
title: {title}
date: {date}
type: "mindmap"
---"""


TOGGLE_CSS = """\
<style>
.mindmap-view-toggle {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  align-items: center;
}
.mindmap-toggle-btn {
  padding: 8px 22px;
  border: 2px solid #49b1f5;
  background: transparent;
  color: #49b1f5;
  border-radius: 22px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  outline: none;
}
.mindmap-toggle-btn:hover {
  background: rgba(73, 177, 245, 0.1);
  transform: translateY(-1px);
}
.mindmap-toggle-btn.active {
  background: #49b1f5;
  color: #fff;
}
.mindmap-tree-text {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 10px;
  padding: 20px 24px;
  font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.9;
  overflow-x: auto;
  white-space: pre;
  color: #24292e;
}
[data-theme="dark"] .mindmap-tree-text {
  background: #1e1e2e;
  border-color: #313244;
  color: #cdd6f4;
}
[data-theme="dark"] .mindmap-toggle-btn {
  border-color: #89b4fa;
  color: #89b4fa;
}
[data-theme="dark"] .mindmap-toggle-btn:hover {
  background: rgba(137, 180, 250, 0.15);
}
[data-theme="dark"] .mindmap-toggle-btn.active {
  background: #89b4fa;
  color: #1e1e2e;
}
/* ---- Editor ---- */
.mindmap-editor-wrapper { display: none; margin-bottom: 16px; }
.mindmap-editor-toolbar {
  display: flex; gap: 6px; flex-wrap: wrap;
  margin-bottom: 0; padding: 8px 12px;
  background: #f6f8fa; border: 1px solid #e1e4e8;
  border-radius: 10px 10px 0 0; border-bottom: none;
}
.mindmap-editor-toolbar button {
  padding: 4px 12px; border: 1px solid #d0d7de;
  background: #fff; border-radius: 6px;
  cursor: pointer; font-size: 13px; transition: all 0.2s; white-space: nowrap;
}
.mindmap-editor-toolbar button:hover { background: #49b1f5; color: #fff; border-color: #49b1f5; }
.mindmap-editor-textarea {
  width: 100%; min-height: 400px; padding: 16px;
  border: 1px solid #e1e4e8; border-radius: 0 0 10px 10px;
  font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 13px; line-height: 1.9; resize: vertical;
  background: #fff; color: #24292e; outline: none;
}
.mindmap-editor-textarea:focus { border-color: #49b1f5; box-shadow: 0 0 0 3px rgba(73,177,245,0.15); }
.mindmap-save-row { display: none; align-items: center; gap: 10px; margin-top: 12px; }
.mindmap-save-btn {
  padding: 10px 28px; border: none; background: #2da44e; color: #fff;
  border-radius: 22px; cursor: pointer; font-size: 14px; font-weight: 600;
  transition: all 0.3s; outline: none;
}
.mindmap-save-btn:hover { background: #1a7f37; transform: translateY(-1px); }
.mindmap-save-btn:disabled { background: #94d3a2; cursor: not-allowed; transform: none; }
.mindmap-save-status { font-size: 13px; }
.mindmap-save-status.success { color: #2da44e; }
.mindmap-save-status.error { color: #cf222e; }
.mindmap-token-overlay {
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); z-index: 9999; justify-content: center; align-items: center;
}
.mindmap-token-dialog {
  background: #fff; border-radius: 12px; padding: 24px;
  max-width: 440px; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.mindmap-token-dialog h3 { margin: 0 0 12px; font-size: 16px; }
.mindmap-token-dialog input {
  width: 100%; padding: 10px 12px; border: 1px solid #d0d7de;
  border-radius: 8px; font-size: 14px; margin-bottom: 8px; box-sizing: border-box;
}
.mindmap-token-dialog .hint { font-size: 12px; color: #656d76; margin-bottom: 16px; }
.mindmap-token-dialog .hint a { color: #49b1f5; }
.mindmap-token-dialog .actions { display: flex; gap: 8px; justify-content: flex-end; }
.mindmap-token-dialog .actions button {
  padding: 6px 16px; border-radius: 8px; border: 1px solid #d0d7de;
  background: #fff; cursor: pointer; font-size: 13px;
}
.mindmap-token-dialog .actions .btn-primary { background: #49b1f5; color: #fff; border-color: #49b1f5; }
[data-theme="dark"] .mindmap-editor-toolbar { background: #1e1e2e; border-color: #313244; }
[data-theme="dark"] .mindmap-editor-toolbar button { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .mindmap-editor-textarea { background: #1e1e2e; border-color: #313244; color: #cdd6f4; }
[data-theme="dark"] .mindmap-token-dialog { background: #1e1e2e; color: #cdd6f4; }
[data-theme="dark"] .mindmap-token-dialog input { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .mindmap-token-dialog .actions button { background: #313244; border-color: #45475a; color: #cdd6f4; }
</style>"""

TOGGLE_JS = """\
<script>
(function() {
  var currentView = 'mindmap', isEditing = false;
  var sourceFilename = '__SOURCE_FILENAME__';
  var owner = '1whistlerrrr', repo = '1whistlerrrr.github.io';
  var editHistory = [], historyIdx = -1;

  window.switchMindmapView = function(view) {
    if (currentView === view && !isEditing) return;
    if (isEditing) exitEditMode(true);
    currentView = view; isEditing = false;
    var btns = document.querySelectorAll('.mindmap-toggle-btn');
    btns.forEach(function(b){b.classList.remove('active');});
    document.getElementById('mindmap-view').style.display = view==='mindmap'?'block':'none';
    document.getElementById('tree-view').style.display = view==='tree'?'block':'none';
    document.getElementById('edit-view').style.display = 'none';
    document.querySelector('.mindmap-editor-wrapper').style.display = 'none';
    document.querySelector('.mindmap-save-row').style.display = 'none';
    if(view==='mindmap'){btns[0].classList.add('active');window.dispatchEvent(new Event('resize'));}
    else{btns[1].classList.add('active');}
    document.getElementById('edit-btn').style.display='inline-flex';
    document.getElementById('cancel-edit-btn').style.display='none';
  };

  window.enterEditMode = function() {
    isEditing = true;
    var btns = document.querySelectorAll('.mindmap-toggle-btn');
    btns.forEach(function(b){b.classList.remove('active');});
    document.getElementById('mindmap-view').style.display='none';
    document.getElementById('tree-view').style.display='none';
    document.getElementById('edit-view').style.display='block';
    document.querySelector('.mindmap-editor-wrapper').style.display='block';
    document.querySelector('.mindmap-save-row').style.display='flex';
    document.getElementById('edit-btn').style.display='none';
    document.getElementById('cancel-edit-btn').style.display='inline-flex';
    document.getElementById('cancel-edit-btn').classList.add('active');
    document.getElementById('save-status').textContent='';
    document.getElementById('save-status').className='mindmap-save-status';
    var ta = document.getElementById('mindmap-textarea');
    editHistory = [ta.value]; historyIdx = 0;
    ta.focus();
  };

  window.exitEditMode = function(discard) {
    if(!discard) return;
    isEditing = false;
    document.getElementById('edit-view').style.display='none';
    document.querySelector('.mindmap-editor-wrapper').style.display='none';
    document.querySelector('.mindmap-save-row').style.display='none';
    document.getElementById('edit-btn').style.display='inline-flex';
    document.getElementById('cancel-edit-btn').style.display='none';
    document.getElementById('cancel-edit-btn').classList.remove('active');
    document.getElementById('tree-view').style.display='block';
    document.querySelectorAll('.mindmap-toggle-btn')[1].classList.add('active');
    currentView = 'tree';
  };

  window.editorCmd = function(cmd) {
    var ta=document.getElementById('mindmap-textarea');
    var s=ta.selectionStart,e=ta.selectionEnd,t=ta.value,sel=t.substring(s,e);
    var wL='',wR='';
    switch(cmd){
      case 'bold':wL='**';wR='**';break;
      case 'strike':wL='~~';wR='~~';break;
      case 'highlight':wL='==';wR='==';break;
      case 'code':wL='`';wR='`';break;
    }
    if(!sel.length){
      var ph={bold:'粗体',strike:'删除线',highlight:'高亮',code:'代码'}[cmd]||'';
      ta.value=t.substring(0,s)+wL+ph+wR+t.substring(e);
      ta.focus();ta.setSelectionRange(s+wL.length,s+wL.length+ph.length);
    }else{
      ta.value=t.substring(0,s)+wL+sel+wR+t.substring(e);
      ta.focus();ta.setSelectionRange(s,e+wL.length+wR.length);
    }
    pushHistory();
  };

  function pushHistory(){
    var ta=document.getElementById('mindmap-textarea');
    editHistory=editHistory.slice(0,historyIdx+1);
    editHistory.push(ta.value);historyIdx=editHistory.length-1;
  }

  window.editorUndo=function(){if(historyIdx>0){historyIdx--;document.getElementById('mindmap-textarea').value=editHistory[historyIdx];}};
  window.editorRedo=function(){if(historyIdx<editHistory.length-1){historyIdx++;document.getElementById('mindmap-textarea').value=editHistory[historyIdx];}};

  document.addEventListener('keydown',function(e){
    if(!isEditing)return;
    if((e.ctrlKey||e.metaKey)&&e.key==='z'&&!e.shiftKey){e.preventDefault();editorUndo();}
    if((e.ctrlKey||e.metaKey)&&(e.key==='y'||(e.key==='z'&&e.shiftKey))){e.preventDefault();editorRedo();}
  });
  document.addEventListener('input',function(e){if(e.target.id==='mindmap-textarea'&&isEditing)pushHistory();});

  function getToken(){try{return localStorage.getItem('gh_mindmap_token')||'';}catch(e){return '';}}
  function setToken(t){try{localStorage.setItem('gh_mindmap_token',t);}catch(e){}}

  window.showTokenDialog=function(){
    document.getElementById('token-overlay').style.display='flex';
    document.getElementById('token-input').value=getToken();
    document.getElementById('token-input').focus();
  };
  window.hideTokenDialog=function(){document.getElementById('token-overlay').style.display='none';};
  window.saveToken=function(){
    var t=document.getElementById('token-input').value.trim();
    if(t){setToken(t);hideTokenDialog();doSave();}
  };

  window.saveToGitHub=function(){
    var token=getToken();
    if(!token){showTokenDialog();return;}
    doSave();
  };

  function utf8_to_b64(str){return btoa(unescape(encodeURIComponent(str)));}

  function doSave(){
    var token=getToken();if(!token)return;
    var btn=document.getElementById('save-btn');
    var status=document.getElementById('save-status');
    btn.disabled=true;status.textContent='⏳ 保存中...';status.className='mindmap-save-status';
    var content=document.getElementById('mindmap-textarea').value;
    var path='source/raw_mindmap/'+sourceFilename;

    fetch('https://api.github.com/repos/'+owner+'/'+repo+'/contents/'+path,{
      headers:{Authorization:'Bearer '+token,Accept:'application/vnd.github+json'}
    }).then(function(r){
      if(!r.ok)throw new Error('获取文件信息失败 ('+r.status+')');
      return r.json();
    }).then(function(data){
      return fetch('https://api.github.com/repos/'+owner+'/'+repo+'/contents/'+path,{
        method:'PUT',
        headers:{Authorization:'Bearer '+token,'Content-Type':'application/json',Accept:'application/vnd.github+json'},
        body:JSON.stringify({message:'✏️ 更新 '+sourceFilename+' (via web editor)',content:utf8_to_b64(content),sha:data.sha})
      });
    }).then(function(r){
      if(!r.ok)throw new Error('提交失败 ('+r.status+')');
      status.textContent='✅ 已保存！GitHub Actions 正在重新部署，约1分钟后生效。';
      status.className='mindmap-save-status success';
      document.querySelector('#tree-view .mindmap-tree-text').textContent=content;
      btn.disabled=false;
    }).catch(function(err){
      status.textContent='❌ '+err.message;
      status.className='mindmap-save-status error';
      btn.disabled=false;
    });
  }
})();
</script>"""

TOGGLE_HTML = """\
<div class="mindmap-view-toggle">
  <button class="mindmap-toggle-btn active" onclick="switchMindmapView('mindmap')">🧠 思维导图</button>
  <button class="mindmap-toggle-btn" onclick="switchMindmapView('tree')">📝 原始文本</button>
  <button id="edit-btn" class="mindmap-toggle-btn" style="border-style:dashed;" onclick="enterEditMode()">✏️ 编辑</button>
  <button id="cancel-edit-btn" class="mindmap-toggle-btn" style="display:none;border-color:#cf222e;color:#cf222e;" onclick="exitEditMode(true)">✕ 取消编辑</button>
</div>

<div id="mindmap-view" class="mindmap-view-content">
{{% markmap %}}
{markmap_body}
{{% endmarkmap %}}
</div>

<div id="tree-view" class="mindmap-view-content" style="display:none;">
<pre class="mindmap-tree-text">{tree_text}</pre>
</div>

<div id="edit-view" class="mindmap-view-content" style="display:none;">
  <div class="mindmap-editor-wrapper">
    <div class="mindmap-editor-toolbar">
      <button onclick="editorCmd('highlight')" title="高亮 == ==">🖍 高亮</button>
      <button onclick="editorCmd('strike')" title="删除线 ~~ ~~"><s>S</s> 删除线</button>
      <button onclick="editorCmd('bold')" title="粗体 ** **"><b>B</b> 粗体</button>
      <button onclick="editorCmd('code')" title="行内代码 ` `">&lt;/&gt; 代码</button>
      <span style="flex:1;"></span>
      <button onclick="editorUndo()" title="撤销 Ctrl+Z">↩ 撤销</button>
      <button onclick="editorRedo()" title="重做 Ctrl+Y">↪ 重做</button>
    </div>
    <textarea id="mindmap-textarea" class="mindmap-editor-textarea" spellcheck="false">{tree_raw}</textarea>
  </div>
  <div class="mindmap-save-row" style="display:none;">
    <button id="save-btn" class="mindmap-save-btn" onclick="saveToGitHub()">💾 保存到 GitHub</button>
    <span id="save-status" class="mindmap-save-status"></span>
  </div>
</div>

<div id="token-overlay" class="mindmap-token-overlay">
  <div class="mindmap-token-dialog">
    <h3>🔑 输入 GitHub Token</h3>
    <input type="password" id="token-input" placeholder="ghp_xxxxxxxxxxxxxxxxxxxx" />
    <div class="hint">
      需要 <code>repo</code> 权限。<br />
      <a href="https://github.com/settings/tokens/new?scopes=repo&description=Mindmap+Editor" target="_blank">→ 点击创建 Classic Token（勾选 repo）</a>
    </div>
    <div class="actions">
      <button onclick="hideTokenDialog()">取消</button>
      <button class="btn-primary" onclick="saveToken()">保存并提交</button>
    </div>
  </div>
</div>
"""


def build_output(title: str, markmap_body: str, tree_text: str, source_filename: str) -> str:
    """构建包含双视图切换 + 在线编辑器的完整页面内容。"""
    tree_escaped = (
        tree_text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .strip()
    )
    tree_raw = tree_text.strip()
    toggle_html = TOGGLE_HTML.format(markmap_body=markmap_body, tree_text=tree_escaped, tree_raw=tree_raw)
    toggle_js = TOGGLE_JS.replace("__SOURCE_FILENAME__", source_filename)
    return f"""## {title}

{TOGGLE_CSS}
{toggle_html}
{toggle_js}"""


def convert_file(input_path: Path, output_path: Path) -> bool:
    """转换单个文件。"""
    try:
        raw_text = input_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [ERROR] 无法读取 {input_path.name}: {e}")
        return False

    if not raw_text.strip():
        print(f"  [SKIP] {input_path.name} 是空文件")
        return False

    # 分离自定义 frontmatter 和树形内容
    body = raw_text
    custom_title = None
    custom_date = None

    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            for line in fm_text.split("\n"):
                line = line.strip()
                if line.startswith("title:"):
                    custom_title = line.split(":", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("date:"):
                    custom_date = line.split(":", 1)[1].strip().strip('"').strip("'")

    # 转换树形内容
    markmap_body = convert_tree_to_markmap(body)
    if not markmap_body:
        print(f"  [SKIP] {input_path.name} 未识别到有效树形内容")
        return False

    title = custom_title or input_path.stem
    frontmatter = generate_frontmatter(title, custom_date)
    page_body = build_output(title, markmap_body, body, input_path.name)

    output_text = f"""{frontmatter}

{page_body}
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    return True


def get_input_files() -> list[Path]:
    """获取所有待处理的原始文件。"""
    if not RAW_DIR.exists():
        return []
    files = []
    for f in RAW_DIR.iterdir():
        if f.is_file() and f.name not in SKIP_FILES:
            files.append(f)
    return sorted(files)


def main():
    force = "--force" in sys.argv
    check_only = "--check" in sys.argv

    input_files = get_input_files()

    if not input_files:
        print("📭 source/raw_mindmap/ 中没有待处理的文件。")
        print(f"   请将树形文本文件放入: {RAW_DIR}")
        return

    cache = load_cache() if not force else {}
    converted = []
    skipped = []
    failed = []

    print(f"🔍 扫描到 {len(input_files)} 个文件\n")

    for input_path in input_files:
        file_key = input_path.name
        current_hash = file_hash(input_path)

        # 检查是否需要重新转换
        if not force and file_key in cache and cache[file_key] == current_hash:
            skipped.append(file_key)
            continue

        if check_only:
            converted.append(file_key)
            continue

        output_name = input_path.stem + ".md"
        output_path = OUTPUT_DIR / output_name

        print(f"🔄 转换: {input_path.name} → {output_name}")
        if convert_file(input_path, output_path):
            converted.append(file_key)
            cache[file_key] = current_hash
        else:
            failed.append(file_key)

    # 保存缓存
    if not check_only:
        save_cache(cache)

    # 清理已删除源文件对应的输出文件
    if not check_only and not force:
        valid_stems = {f.stem for f in input_files}
        if OUTPUT_DIR.exists():
            for out_file in OUTPUT_DIR.iterdir():
                if out_file.suffix == ".md" and out_file.stem not in valid_stems:
                    print(f"🗑️  清理孤立输出: {out_file.name}")
                    out_file.unlink()

    # 汇总
    print()
    print("=" * 50)
    if check_only:
        if converted:
            print(f"📋 待转换文件 ({len(converted)} 个):")
            for f in converted:
                print(f"   → {f}")
        else:
            print("✅ 所有文件已是最新，无需转换。")
    else:
        if converted:
            print(f"✅ 成功转换: {len(converted)} 个")
        if skipped:
            print(f"⏭️  跳过（未变化）: {len(skipped)} 个")
        if failed:
            print(f"❌ 失败: {len(failed)} 个")
            for f in failed:
                print(f"   → {f}")
        if not converted and not failed:
            print("✅ 所有文件已是最新，无需转换。")


if __name__ == "__main__":
    main()
