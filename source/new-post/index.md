---
title: 新增页面
date: 2026-07-29 10:00:00
type: "newpost"
---

## 📝 新增页面

填写内容后点击"提交"，输入密码 `lcy666` 即可创建新文章。

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
    <span id="np-status"></span>
  </div>

  <!-- 密码弹窗 -->
  <div id="np-pwd-overlay">
    <div class="np-pwd-dialog">
      <h4>🔐 输入密码</h4>
      <p id="np-pwd-msg" style="color:#cf222e;font-size:12px;margin:0 0 8px;"></p>
      <input type="password" id="np-pwd-input" placeholder="请输入密码" />
      <div class="np-pwd-actions">
        <button id="np-pwd-cancel">取消</button>
        <button id="np-pwd-confirm" class="np-btn-primary">确认提交</button>
      </div>
    </div>
  </div>
</div>

<style>
#newpost-form-container { max-width: 720px; margin: 0 auto; }
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
#np-status { font-size: 13px; }
#np-status.np-status-success { color: #2da44e; }
#np-status.np-status-error { color: #cf222e; }
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
[data-theme="dark"] .np-pwd-dialog { background: #1e1e2e; }
[data-theme="dark"] .np-pwd-dialog h4 { color: #cdd6f4; }
[data-theme="dark"] #np-pwd-input { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .np-pwd-actions button { background: #313244; border-color: #45475a; color: #cdd6f4; }
</style>

<script>
(function() {
  var OWNER = '1whistlerrrr', REPO = '1whistlerrrr.github.io';
  var POSTS_DIR = 'source/_posts/';
  var ENCRYPTED_TOKEN = 'CwsJaWEFNFQNUGZXCDISck5xKCIuQ1UGFBo/V3NvBS8YBAUCHDYRZw==';

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
  function getCachedToken() { try { return localStorage.getItem('gh_mindmap_token')||''; } catch(e) { return ''; } }
  function setCachedToken(t) { try { localStorage.setItem('gh_mindmap_token',t); } catch(e) {} }
  function resolveToken(pwd) {
    if (ENCRYPTED_TOKEN && pwd && pwd.length<50) {
      var tok = decryptToken(ENCRYPTED_TOKEN, pwd);
      if (!tok||(!tok.startsWith('ghp_')&&!tok.startsWith('github_pat_'))) return null;
      setCachedToken(tok); return tok;
    }
    return getCachedToken();
  }

  function showPwdDialog(msg) {
    document.getElementById('np-pwd-overlay').style.display='flex';
    document.getElementById('np-pwd-msg').textContent=msg||'';
    document.getElementById('np-pwd-input').value='';
    document.getElementById('np-pwd-input').focus();
  }
  function hidePwdDialog() { document.getElementById('np-pwd-overlay').style.display='none'; }

  function slugify(title) {
    return title.toLowerCase().replace(/\s+/g,'-').replace(/[^\w一-鿿\-]/g,'').replace(/-+/g,'-').replace(/^-|-$/g,'').substring(0,60) || 'untitled';
  }

  function getDateStr() {
    var d = new Date();
    var pad = function(n) { return n<10?'0'+n:''+n; };
    return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());
  }

  document.getElementById('np-submit-btn').addEventListener('click', function() {
    var title = document.getElementById('np-title').value.trim();
    var tags = document.getElementById('np-tags').value.trim();
    var content = document.getElementById('np-content').value.trim();
    if (!title) { showStatus('请输入文章标题', 'error'); return; }
    if (!content) { showStatus('请输入文章内容', 'error'); return; }

    var cached = getCachedToken();
    if (cached) { doSubmit(null, title, tags, content); return; }
    showPwdDialog('');
  });

  document.getElementById('np-pwd-cancel').addEventListener('click', hidePwdDialog);
  document.getElementById('np-pwd-confirm').addEventListener('click', function() {
    var pwd = document.getElementById('np-pwd-input').value.trim();
    if (!pwd) { showPwdDialog('请输入密码'); return; }
    hidePwdDialog();
    var title = document.getElementById('np-title').value.trim();
    var tags = document.getElementById('np-tags').value.trim();
    var content = document.getElementById('np-content').value.trim();
    doSubmit(pwd, title, tags, content);
  });
  document.getElementById('np-pwd-input').addEventListener('keydown', function(e) {
    if (e.key==='Enter') document.getElementById('np-pwd-confirm').click();
  });

  function showStatus(msg, type) {
    var el = document.getElementById('np-status');
    el.textContent = msg;
    el.className = type === 'success' ? 'np-status-success' : (type === 'error' ? 'np-status-error' : '');
  }

  function doSubmit(pwd, title, tags, content) {
    var token = resolveToken(pwd);
    if (!token) { showPwdDialog('密码错误，请重试'); return; }

    var slug = slugify(title);
    var dateStr = getDateStr();
    var filename = dateStr + '-' + slug + '.md';
    var tagsArr = tags ? tags.split(',').map(function(t) { return t.trim(); }).filter(Boolean) : [];
    var tagsYaml = tagsArr.length ? '\ntags:\n' + tagsArr.map(function(t) { return '  - ' + t; }).join('\n') : '';

    var frontmatter =
      '---\n' +
      'title: ' + title + '\n' +
      'date: ' + dateStr + ' ' + new Date().toTimeString().slice(0,8) + '\n' +
      tagsYaml + '\n' +
      '---\n\n' +
      content + '\n';

    var btn = document.getElementById('np-submit-btn');
    var statusEl = document.getElementById('np-status');
    btn.disabled = true;
    showStatus('⏳ 提交中…', '');

    var apiPath = POSTS_DIR + filename;
    var apiUrl = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + apiPath;

    function onError(err) {
      showStatus('❌ ' + err, 'error');
      btn.disabled = false;
    }

    // 先检查文件是否已存在
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
      // 文件不存在，创建
      var putXhr = new XMLHttpRequest();
      putXhr.open('PUT', apiUrl, true);
      putXhr.setRequestHeader('Authorization', 'Bearer ' + token);
      putXhr.setRequestHeader('Content-Type', 'application/json');
      putXhr.setRequestHeader('Accept', 'application/vnd.github+json');
      var body = {
        message: '✏️ 新增文章：' + title + ' (via web editor)',
        content: btoa(unescape(encodeURIComponent(frontmatter)))
      };
      putXhr.onload = function() {
        if (putXhr.status === 200 || putXhr.status === 201) {
          showStatus('✅ 文章已提交！GitHub Actions 正在部署，约1分钟后在首页可见。', 'success');
          document.getElementById('np-title').value = '';
          document.getElementById('np-tags').value = '';
          document.getElementById('np-content').value = '';
        } else {
          var msg = '提交失败 (' + putXhr.status + ')';
          try { var d = JSON.parse(putXhr.responseText); if (d.message) msg = d.message; } catch(e) {}
          onError(msg);
        }
        btn.disabled = false;
      };
      putXhr.onerror = function() { onError('网络错误'); };
      putXhr.send(JSON.stringify(body));
    };
    checkXhr.onerror = function() { onError('网络错误'); };
    checkXhr.send();
  }
})();
</script>
