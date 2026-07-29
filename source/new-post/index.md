---
title: 新增页面
date: 2026-07-29 10:00:00
type: "newpost"
---

## 📝 新增 / 编辑页面

填写内容后提交需验证身份。点击下方列表的"编辑"按钮可修改已有文章。

<div id="newpost-form-container">
  <div class="np-field">
    <label for="np-title">文章标题 <span style="color:#cf222e;">*</span></label>
    <input type="text" id="np-title" placeholder="输入文章标题…" maxlength="100" />
  </div>

  <div class="np-field">
    <label for="np-tags">标签（逗号分隔）</label>
    <input type="text" id="np-tags" placeholder="例如：AI, Java, 工具" maxlength="200" />
  </div>

  <div class="np-field">
    <label for="np-content">内容 <span style="color:#cf222e;">*</span> <small>（Markdown 格式）</small></label>
    <textarea id="np-content" rows="14" placeholder="用 Markdown 写文章内容…" spellcheck="false"></textarea>
  </div>

  <div style="display:flex;align-items:center;gap:12px;margin-top:8px;">
    <button id="np-submit-btn">💾 提交到博客</button>
    <button id="np-cancel-edit-btn" style="display:none;padding:8px 20px;background:none;border:1px solid #999;color:#999;border-radius:22px;cursor:pointer;font-size:13px;">取消编辑</button>
    <span id="np-status"></span>
  </div>
</div>

<hr style="margin:40px 0 24px;border-color:#eee;">

## 📋 文章管理

<div id="np-delete-container">
  <div id="np-posts-list"><p class="np-loading">加载文章列表中…</p></div>
</div>

<!-- 密码弹窗 -->
<div id="np-pwd-overlay">
  <div class="np-pwd-dialog">
    <h4 id="np-pwd-title">🔐 输入密码</h4>
    <p id="np-pwd-msg" style="color:#cf222e;font-size:12px;margin:0 0 8px;"></p>
    <input type="password" id="np-pwd-input" placeholder="请输入密码" />
    <div class="np-pwd-actions">
      <button id="np-pwd-cancel">取消</button>
      <button id="np-pwd-confirm" class="np-btn-primary">确认</button>
    </div>
  </div>
</div>

<style>
#newpost-form-container, #np-delete-container { max-width: 720px; margin: 0 auto; }
.np-field { margin-bottom: 16px; }
.np-field label { display: block; margin-bottom: 4px; font-weight: 600; color: #333; font-size: 14px; }
.np-field small { font-weight: 400; color: #888; }
.np-field input, .np-field textarea { width: 100%; padding: 10px 14px;
  border: 1px solid #ddd; border-radius: 10px; font-size: 14px;
  outline: none; box-sizing: border-box; font-family: inherit; background: #fff; color: #333; }
.np-field input:focus, .np-field textarea:focus { border-color: #9FA1FF; box-shadow: 0 0 0 3px rgba(159,161,255,.15); }
.np-field textarea { resize: vertical; min-height: 300px; line-height: 1.7; }
#np-submit-btn { padding: 10px 32px; background: #2da44e; color: #fff; border: none;
  border-radius: 22px; cursor: pointer; font-size: 15px; font-weight: 600; transition: all .3s; }
#np-submit-btn:hover { background: #1a7f37; transform: translateY(-1px); }
#np-submit-btn:disabled { background: #94d3a2; cursor: not-allowed; transform: none; }
#np-cancel-edit-btn:hover { border-color:#cf222e;color:#cf222e; }
#np-status { font-size: 13px; }
.np-status-success { color: #2da44e; }
.np-status-error { color: #cf222e; }
.np-loading { text-align: center; color: #999; padding: 24px 0; font-size: 14px; }
.np-post-item { display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px; border: 1px solid #eee; border-radius: 8px; margin-bottom: 6px; }
.np-post-item:hover { background: #fafafa; }
.np-post-info { flex: 1; min-width: 0; }
.np-post-name { font-size: 14px; color: #333; font-weight: 500;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.np-post-date { font-size: 11px; color: #999; margin-top: 2px; }
.np-post-actions { display: flex; gap: 6px; flex-shrink: 0; margin-left: 12px; }
.np-edit-btn { padding: 4px 14px; background: none; border: 1px solid #9FA1FF;
  color: #9FA1FF; border-radius: 16px; cursor: pointer; font-size: 12px;
  white-space: nowrap; transition: all .2s; }
.np-edit-btn:hover { background: #9FA1FF; color: #fff; }
.np-delete-btn { padding: 4px 14px; background: none; border: 1px solid #cf222e;
  color: #cf222e; border-radius: 16px; cursor: pointer; font-size: 12px;
  white-space: nowrap; transition: all .2s; }
.np-delete-btn:hover { background: #cf222e; color: #fff; }
#np-pwd-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,.5); z-index: 9999; justify-content: center; align-items: center; }
.np-pwd-dialog { background: #fff; border-radius: 12px; padding: 24px;
  max-width: 400px; width: 90%; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,.2); }
.np-pwd-dialog h4 { margin: 0 0 12px; font-size: 16px; color: #333; }
#np-pwd-input { padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px;
  font-size: 14px; width: 200px; text-align: center; outline: none; }
#np-pwd-input:focus { border-color: #9FA1FF; }
.np-pwd-actions { margin-top: 12px; display: flex; gap: 8px; justify-content: center; }
.np-pwd-actions button { padding: 6px 16px; border-radius: 8px; border: 1px solid #ddd;
  background: #fff; cursor: pointer; font-size: 13px; }
.np-btn-primary { background: #9FA1FF !important; color: #fff !important; border-color: #9FA1FF !important; }
[data-theme="dark"] .np-field label { color: #cdd6f4; }
[data-theme="dark"] .np-field input, [data-theme="dark"] .np-field textarea { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .np-post-item { border-color: #313244; }
[data-theme="dark"] .np-post-item:hover { background: #252536; }
[data-theme="dark"] .np-post-name { color: #cdd6f4; }
[data-theme="dark"] .np-pwd-dialog { background: #1e1e2e; }
[data-theme="dark"] .np-pwd-dialog h4 { color: #cdd6f4; }
[data-theme="dark"] #np-pwd-input { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .np-pwd-actions button { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .np-edit-btn { border-color: #89b4fa; color: #89b4fa; }
[data-theme="dark"] .np-edit-btn:hover { background: #89b4fa; color: #1e1e2e; }
</style>

<script>
(function() {
  var OWNER = '1whistlerrrr', REPO = '1whistlerrrr.github.io';
  var POSTS_API = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/source/_posts/';
  var ENCRYPTED_TOKEN = 'CwsJaWEFNFQNUGZXCDISck5xKCIuQ1UGFBo/V3NvBS8YBAUCHDYRZw==';
  var pendingAction = null; // 'create' | 'update' | {type:'delete', ...}
  var editingFile = null; // null or {path, sha, name, originalTitle}

  function decryptToken(encB64, pwd) {
    try {
      var b = atob(encB64), bytes = new Uint8Array(b.length);
      for (var i=0;i<b.length;i++) bytes[i]=b.charCodeAt(i);
      var key = pwd.repeat(Math.ceil(bytes.length/pwd.length)).slice(0,bytes.length);
      var r = new Uint8Array(bytes.length);
      for (var i=0;i<bytes.length;i++) r[i]=bytes[i]^key.charCodeAt(i);
      return String.fromCharCode.apply(null,r);
    } catch(e) { return ''; }
  }
  function setCachedToken(t) { try { localStorage.setItem('gh_mindmap_token',t); } catch(e) {} }
  function resolveToken(pwd) {
    if (ENCRYPTED_TOKEN && pwd && pwd.length<50) {
      var tok = decryptToken(ENCRYPTED_TOKEN, pwd);
      if (!tok||(!tok.startsWith('ghp_')&&!tok.startsWith('github_pat_'))) return null;
      setCachedToken(tok); return tok;
    }
    return null;
  }

  function showPwd(title, msg) {
    document.getElementById('np-pwd-title').textContent = title || '🔐 输入密码';
    document.getElementById('np-pwd-msg').textContent = msg || '';
    document.getElementById('np-pwd-overlay').style.display = 'flex';
    document.getElementById('np-pwd-input').value = '';
    document.getElementById('np-pwd-input').focus();
  }
  function hidePwd() { document.getElementById('np-pwd-overlay').style.display = 'none'; }

  function showStatus(msg, type) {
    var el = document.getElementById('np-status');
    el.textContent = msg;
    el.className = type === 'success' ? 'np-status-success' : (type === 'error' ? 'np-status-error' : '');
  }

  function resetForm() {
    document.getElementById('np-title').value = '';
    document.getElementById('np-tags').value = '';
    document.getElementById('np-content').value = '';
    document.getElementById('np-submit-btn').textContent = '💾 提交到博客';
    document.getElementById('np-cancel-edit-btn').style.display = 'none';
    editingFile = null;
    showStatus('', '');
  }

  function enterEditMode(path, sha, name, title, tags, content) {
    editingFile = { path: path, sha: sha, name: name, originalTitle: title };
    document.getElementById('np-title').value = title;
    document.getElementById('np-tags').value = tags;
    document.getElementById('np-content').value = content;
    document.getElementById('np-submit-btn').textContent = '💾 更新文章';
    document.getElementById('np-cancel-edit-btn').style.display = 'inline-block';
    showStatus('正在编辑：' + name + '（修改后提交需密码验证）', '');
    document.getElementById('np-title').focus();
  }

  function slugify(title) {
    return title.toLowerCase().replace(/\s+/g,'-').replace(/[^\w一-鿿\-]/g,'').replace(/-+/g,'-').replace(/^-|-$/g,'').substring(0,60) || 'untitled';
  }
  function getDateStr() {
    var d = new Date();
    var pad = function(n) { return n<10?'0'+n:''+n; };
    return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());
  }

  // ============ Submit (create or update) ============
  document.getElementById('np-submit-btn').addEventListener('click', function() {
    var title = document.getElementById('np-title').value.trim();
    var content = document.getElementById('np-content').value.trim();
    if (!title) { showStatus('请输入文章标题', 'error'); return; }
    if (!content) { showStatus('请输入文章内容', 'error'); return; }
    pendingAction = editingFile ? 'update' : 'create';
    showPwd(editingFile ? '🔐 更新文章 - 输入密码' : '🔐 创建文章 - 输入密码');
  });

  document.getElementById('np-cancel-edit-btn').addEventListener('click', function() { resetForm(); });

  function buildFrontmatter(title, tagsStr) {
    var tagsArr = tagsStr ? tagsStr.split(',').map(function(t) { return t.trim(); }).filter(Boolean) : [];
    var tagsYaml = tagsArr.length ? '\ntags:\n' + tagsArr.map(function(t) { return '  - ' + t; }).join('\n') : '';
    var dateStr = editingFile ? (editingFile.originalTitle || getDateStr()) : getDateStr();
    return '---\n' +
      'title: ' + title + '\n' +
      'date: ' + dateStr + ' ' + new Date().toTimeString().slice(0,8) + '\n' +
      tagsYaml + '\n' +
      '---\n\n';
  }

  function doCreate(pwd) {
    var token = resolveToken(pwd);
    if (!token) { showPwd('🔐 密码错误', '密码错误，请重试'); pendingAction = null; return; }

    var title = document.getElementById('np-title').value.trim();
    var tags = document.getElementById('np-tags').value.trim();
    var content = document.getElementById('np-content').value.trim();
    var slug = slugify(title);
    var dateStr = getDateStr();
    var filename = dateStr + '-' + slug + '.md';
    var frontmatter = buildFrontmatter(title, tags) + content + '\n';

    var btn = document.getElementById('np-submit-btn');
    btn.disabled = true;
    showStatus('⏳ 提交中…', '');

    var apiUrl = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/source/_posts/' + filename;
    var checkXhr = new XMLHttpRequest();
    checkXhr.open('GET', apiUrl, true);
    checkXhr.setRequestHeader('Authorization', 'Bearer ' + token);
    checkXhr.setRequestHeader('Accept', 'application/vnd.github+json');
    checkXhr.onload = function() {
      if (checkXhr.status === 200) {
        showStatus('❌ 文件已存在：' + filename, 'error');
        btn.disabled = false;
        return;
      }
      var putXhr = new XMLHttpRequest();
      putXhr.open('PUT', apiUrl, true);
      putXhr.setRequestHeader('Authorization', 'Bearer ' + token);
      putXhr.setRequestHeader('Content-Type', 'application/json');
      putXhr.setRequestHeader('Accept', 'application/vnd.github+json');
      var body = { message: '✏️ 新增文章：' + title + ' (via web editor)',
        content: btoa(unescape(encodeURIComponent(frontmatter))) };
      putXhr.onload = function() {
        if (putXhr.status === 200 || putXhr.status === 201) {
          showStatus('✅ 文章已提交！', 'success');
          resetForm(); loadPosts();
        } else {
          var msg = '提交失败 (' + putXhr.status + ')';
          try { var d = JSON.parse(putXhr.responseText); if (d.message) msg = d.message; } catch(e) {}
          showStatus('❌ ' + msg, 'error');
        }
        btn.disabled = false;
      };
      putXhr.onerror = function() { showStatus('❌ 网络错误', 'error'); btn.disabled = false; };
      putXhr.send(JSON.stringify(body));
    };
    checkXhr.onerror = function() { showStatus('❌ 网络错误', 'error'); btn.disabled = false; };
    checkXhr.send();
  }

  function doUpdate(pwd) {
    var token = resolveToken(pwd);
    if (!token || !editingFile) { showPwd('🔐 密码错误', '密码错误，请重试'); pendingAction = null; return; }

    var title = document.getElementById('np-title').value.trim();
    var tags = document.getElementById('np-tags').value.trim();
    var content = document.getElementById('np-content').value.trim();
    var frontmatter = buildFrontmatter(title, tags) + content + '\n';

    var btn = document.getElementById('np-submit-btn');
    btn.disabled = true;
    showStatus('⏳ 更新中…', '');

    var apiUrl = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + editingFile.path;
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', apiUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/vnd.github+json');
    var body = {
      message: '✏️ 更新文章：' + title + ' (via web editor)',
      content: btoa(unescape(encodeURIComponent(frontmatter))),
      sha: editingFile.sha
    };
    xhr.onload = function() {
      if (xhr.status === 200 || xhr.status === 201) {
        showStatus('✅ 文章已更新！', 'success');
        resetForm(); loadPosts();
      } else {
        var msg = '更新失败 (' + xhr.status + ')';
        try { var d = JSON.parse(xhr.responseText); if (d.message) msg = d.message; } catch(e) {}
        showStatus('❌ ' + msg, 'error');
      }
      btn.disabled = false;
    };
    xhr.onerror = function() { showStatus('❌ 网络错误', 'error'); btn.disabled = false; };
    xhr.send(JSON.stringify(body));
  }

  // ============ Edit Post ============
  function startEdit(path, sha, name) {
    showStatus('⏳ 加载文章内容…', '');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + path, true);
    xhr.setRequestHeader('Accept', 'application/vnd.github+json');
    xhr.onload = function() {
      if (xhr.status !== 200) { showStatus('❌ 加载失败 (' + xhr.status + ')', 'error'); return; }
      try {
        var d = JSON.parse(xhr.responseText);
        var raw = decodeURIComponent(escape(atob(d.content.replace(/\s/g, ''))));
        // 解析 frontmatter
        var title = '', tags = '', content = raw;
        if (raw.indexOf('---') === 0) {
          var endIdx = raw.indexOf('---', 3);
          if (endIdx > 0) {
            var fm = raw.substring(3, endIdx).trim();
            content = raw.substring(endIdx + 3).trim();
            fm.split('\n').forEach(function(line) {
              var m;
              if (m = line.match(/^title:\s*(.+)/i)) title = m[1].trim().replace(/^['"]|['"]$/g, '');
              if (m = line.match(/^tags:\s*$/i)) tags = '';
              if (m = line.match(/^\s*-\s*(.+)/)) {
                if (tags !== undefined) tags += (tags ? ', ' : '') + m[1].trim();
              }
            });
          }
        }
        enterEditMode(path, d.sha, name, title, tags, content);
      } catch(e) {
        showStatus('❌ 解析失败', 'error');
        // fallback: just load raw content
        var raw2 = decodeURIComponent(escape(atob(JSON.parse(xhr.responseText).content.replace(/\s/g, ''))));
        enterEditMode(path, sha, name, '', '', raw2);
      }
    };
    xhr.onerror = function() { showStatus('❌ 网络错误', 'error'); };
    xhr.send();
  }

  // ============ Delete Post ============
  function loadPosts() {
    var list = document.getElementById('np-posts-list');
    list.innerHTML = '<p class="np-loading">加载文章列表中…</p>';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', POSTS_API + '?t=' + Date.now(), true);
    xhr.setRequestHeader('Accept', 'application/vnd.github+json');
    xhr.onload = function() {
      if (xhr.status !== 200) { list.innerHTML = '<p class="np-loading">加载失败 (' + xhr.status + ')</p>'; return; }
      try {
        var files = JSON.parse(xhr.responseText);
        if (!Array.isArray(files) || files.length === 0) { list.innerHTML = '<p class="np-loading">暂无文章</p>'; return; }
        var posts = files.filter(function(f) { return f.name.endsWith('.md'); });
        posts.sort(function(a, b) { return b.name.localeCompare(a.name); });
        var h = '';
        posts.forEach(function(p) {
          var dateMatch = p.name.match(/^(\d{4}-\d{2}-\d{2})/);
          var dateStr = dateMatch ? dateMatch[1] : '';
          var titleStr = p.name.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}-/, '');
          h += '<div class="np-post-item">' +
            '<div class="np-post-info">' +
            '<div class="np-post-name">' + escapeHtml(titleStr) + '</div>' +
            (dateStr ? '<div class="np-post-date">' + dateStr + '</div>' : '') +
            '</div>' +
            '<div class="np-post-actions">' +
            '<button class="np-edit-btn" data-path="' + escapeHtml(p.path) + '" data-sha="' + escapeHtml(p.sha) + '" data-name="' + escapeHtml(p.name) + '">✏️ 编辑</button>' +
            '<button class="np-delete-btn" data-path="' + escapeHtml(p.path) + '" data-sha="' + escapeHtml(p.sha) + '" data-name="' + escapeHtml(p.name) + '">🗑 删除</button>' +
            '</div>' +
            '</div>';
        });
        list.innerHTML = h;
        list.querySelectorAll('.np-edit-btn').forEach(function(btn) {
          btn.addEventListener('click', function() {
            startEdit(this.getAttribute('data-path'), this.getAttribute('data-sha'), this.getAttribute('data-name'));
          });
        });
        list.querySelectorAll('.np-delete-btn').forEach(function(btn) {
          btn.addEventListener('click', function() {
            startDelete(this.getAttribute('data-path'), this.getAttribute('data-sha'), this.getAttribute('data-name'));
          });
        });
      } catch(e) { list.innerHTML = '<p class="np-loading">解析失败</p>'; }
    };
    xhr.onerror = function() { list.innerHTML = '<p class="np-loading">加载失败（网络错误）</p>'; };
    xhr.send();
  }

  function escapeHtml(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

  function startDelete(path, sha, name) {
    if (!confirm('⚠️ 确定要删除这篇文章吗？此操作不可撤销。\n\n' + name)) return;
    pendingAction = { type: 'delete', path: path, sha: sha, name: name };
    showPwd('🔐 删除文章 - 输入密码', '将删除：' + name);
  }

  function doDelete(pwd, item) {
    var token = resolveToken(pwd);
    if (!token) { showPwd('🔐 密码错误', '密码错误，请重试'); pendingAction = null; return; }
    showStatus('⏳ 删除中…', '');
    var apiUrl = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + item.path;
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', apiUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/vnd.github+json');
    var body = { message: '🗑️ 删除文章：' + item.name + ' (via web editor)', sha: item.sha };
    xhr.onload = function() {
      if (xhr.status === 200 || xhr.status === 204) {
        showStatus('✅ 已删除：' + item.name, 'success');
        loadPosts();
      } else {
        var msg = '删除失败 (' + xhr.status + ')';
        try { var d = JSON.parse(xhr.responseText); if (d.message) msg = d.message; } catch(e) {}
        showStatus('❌ ' + msg, 'error');
      }
    };
    xhr.onerror = function() { showStatus('❌ 网络错误', 'error'); };
    xhr.send(JSON.stringify(body));
  }

  // ============ Password confirm ============
  document.getElementById('np-pwd-cancel').addEventListener('click', function() { hidePwd(); pendingAction = null; });
  document.getElementById('np-pwd-confirm').addEventListener('click', function() {
    var pwd = document.getElementById('np-pwd-input').value.trim();
    if (!pwd) { showPwd('🔐 请输入密码', '请输入密码'); return; }
    hidePwd();
    if (pendingAction === 'create') { doCreate(pwd); }
    else if (pendingAction === 'update') { doUpdate(pwd); }
    else if (pendingAction && pendingAction.type === 'delete') { doDelete(pwd, pendingAction); }
    pendingAction = null;
  });
  document.getElementById('np-pwd-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') document.getElementById('np-pwd-confirm').click();
  });

  // ============ Init ============
  loadPosts();
})();
</script>
