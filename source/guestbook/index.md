---
title: 留言板
date: 2026-07-29 10:00:00
type: "guestbook"
---

## 💬 留言板

欢迎留言！鼠标悬停留言可看到删除按钮（需密码验证）。

<div id="guestbook-standalone">
  <div id="gb-page-comments-list"><p class="gb-loading">加载中…</p></div>

  <div class="gb-page-form">
    <input type="text" id="gb-page-input-name" placeholder="昵称（选填）" maxlength="30" />
    <textarea id="gb-page-input-msg" placeholder="写留言…" rows="3" maxlength="500"></textarea>
    <div class="gb-page-form-row">
      <span id="gb-page-char-count">0/500</span>
      <button id="gb-page-submit-btn" class="gb-page-submit-btn">发送留言</button>
    </div>
    <p id="gb-page-status"></p>
  </div>

  <div id="gb-page-pwd-overlay" class="gb-page-pwd-overlay">
    <div class="gb-page-pwd-dialog">
      <h4 id="gb-page-pwd-title">🔐 输入密码</h4>
      <p id="gb-page-pwd-msg" style="color:#cf222e;font-size:12px;margin:0 0 8px;"></p>
      <input type="password" id="gb-page-pwd-input" placeholder="请输入密码" />
      <div class="gb-page-pwd-actions">
        <button id="gb-page-pwd-cancel">取消</button>
        <button id="gb-page-pwd-confirm" class="gb-page-btn-primary">确认</button>
      </div>
    </div>
  </div>
</div>

<style>
#guestbook-standalone { max-width: 680px; margin: 0 auto; }
#gb-page-comments-list { min-height: 80px; margin-bottom: 24px; }
.gb-page-loading, .gb-page-empty { text-align: center; color: #999; padding: 32px 0; font-size: 14px; }
.gb-page-comment-item { position: relative; padding: 14px 0; border-bottom: 1px solid #eee; }
.gb-page-comment-item:last-child { border-bottom: none; }
.gb-page-comment-meta { font-size: 12px; color: #888; margin-bottom: 4px; }
.gb-page-comment-body { font-size: 15px; color: #333; line-height: 1.6; word-break: break-word; padding-right: 28px; }
.gb-page-comment-delete { position: absolute; top: 14px; right: 0; background: none; border: none;
  color: #ccc; cursor: pointer; font-size: 18px; line-height: 1; padding: 2px 6px;
  opacity: 0; transition: opacity .2s; }
.gb-page-comment-item:hover .gb-page-comment-delete { opacity: 1; }
.gb-page-comment-delete:hover { color: #cf222e; }
.gb-page-form { background: #f8f9fa; border-radius: 12px; padding: 16px 20px; }
#gb-page-input-name { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px;
  font-size: 14px; margin-bottom: 10px; box-sizing: border-box; outline: none; background: #fff; }
#gb-page-input-name:focus { border-color: #9FA1FF; }
#gb-page-input-msg { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px;
  font-size: 14px; resize: vertical; box-sizing: border-box; outline: none; font-family: inherit; background: #fff; }
#gb-page-input-msg:focus { border-color: #9FA1FF; }
.gb-page-form-row { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }
#gb-page-char-count { font-size: 12px; color: #999; }
.gb-page-submit-btn { padding: 10px 28px; background: #9FA1FF; color: #fff; border: none;
  border-radius: 22px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all .3s; }
.gb-page-submit-btn:hover { background: #7c7eff; }
.gb-page-submit-btn:disabled { background: #ccc; cursor: not-allowed; }
#gb-page-status { font-size: 12px; margin: 6px 0 0; min-height: 18px; }
.gb-page-status-success { color: #2da44e; }
.gb-page-status-error { color: #cf222e; }
.gb-page-pwd-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,.5); z-index: 9999; justify-content: center; align-items: center; }
.gb-page-pwd-dialog { background: #fff; border-radius: 12px; padding: 24px; text-align: center;
  box-shadow: 0 8px 32px rgba(0,0,0,.2); }
.gb-page-pwd-dialog h4 { margin: 0 0 12px; font-size: 16px; color: #333; }
#gb-page-pwd-input { padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px;
  font-size: 14px; width: 200px; text-align: center; outline: none; }
#gb-page-pwd-input:focus { border-color: #9FA1FF; }
.gb-page-pwd-actions { margin-top: 12px; display: flex; gap: 8px; justify-content: center; }
.gb-page-pwd-actions button { padding: 6px 16px; border-radius: 8px; border: 1px solid #ddd;
  background: #fff; cursor: pointer; font-size: 13px; }
.gb-page-btn-primary { background: #9FA1FF !important; color: #fff !important; border-color: #9FA1FF !important; }
[data-theme="dark"] .gb-page-comment-item { border-color: #313244; }
[data-theme="dark"] .gb-page-comment-meta { color: #6c7086; }
[data-theme="dark"] .gb-page-comment-body { color: #cdd6f4; }
[data-theme="dark"] .gb-page-form { background: #1e1e2e; }
[data-theme="dark"] #gb-page-input-name, [data-theme="dark"] #gb-page-input-msg { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .gb-page-pwd-dialog { background: #1e1e2e; }
[data-theme="dark"] .gb-page-pwd-dialog h4 { color: #cdd6f4; }
[data-theme="dark"] #gb-page-pwd-input { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .gb-page-pwd-actions button { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .gb-page-comment-delete { color: #585b70; }
[data-theme="dark"] .gb-page-comment-delete:hover { color: #e06c75; }
</style>

<script>
(function() {
  var OWNER = '1whistlerrrr', REPO = '1whistlerrrr.github.io';
  var COMMENTS_PATH = 'source/_data/comments.json';
  var API_URL = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + COMMENTS_PATH;
  var ENCRYPTED_TOKEN = 'CwsJaWEFNFQNUGZXCDISck5xKCIuQ1UGFBo/V3NvBS8YBAUCHDYRZw==';
  var COMMENTS_CACHE = null, FILE_SHA = null;
  var pendingAction = null;

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

  // 用 GitHub API 读取文件（不走 raw.githubusercontent.com，无 CDN 缓存延迟）
  function fetchComments(cb) {
    var x = new XMLHttpRequest();
    x.open('GET', API_URL, true);
    x.setRequestHeader('Accept', 'application/vnd.github+json');
    x.onload = function() {
      if (x.status === 200) {
        try {
          var d = JSON.parse(x.responseText);
          if (d.content) {
            var raw = atob(d.content.replace(/\s/g, ''));
            COMMENTS_CACHE = JSON.parse(decodeURIComponent(escape(raw)));
            FILE_SHA = d.sha;
          }
        } catch(e) { COMMENTS_CACHE = []; }
      } else {
        COMMENTS_CACHE = [];
      }
      cb(COMMENTS_CACHE);
    };
    x.onerror = function() { cb(COMMENTS_CACHE || []); };
    x.send();
  }

  function saveComments(token, comments, sha, commitMsg, cb, errCb) {
    var x = new XMLHttpRequest();
    x.open('PUT', API_URL, true);
    x.setRequestHeader('Authorization', 'Bearer ' + token);
    x.setRequestHeader('Content-Type', 'application/json');
    x.setRequestHeader('Accept', 'application/vnd.github+json');
    var body = { message: commitMsg, content: btoa(unescape(encodeURIComponent(JSON.stringify(comments, null, 2)))) };
    if (sha) body.sha = sha;
    x.onload = function() {
      if (x.status === 200 || x.status === 201) {
        var d = JSON.parse(x.responseText);
        FILE_SHA = d.content ? d.content.sha : sha;
        cb();
      } else {
        errCb('提交失败 (' + x.status + ')');
      }
    };
    x.onerror = function() { errCb('网络错误'); };
    x.send(JSON.stringify(body));
  }

  function formatTime(iso) { var d = new Date(iso); var p = function(n) { return n < 10 ? '0' + n : '' + n; }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()); }
  function escapeHtml(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

  function renderComments(comments) {
    var list = document.getElementById('gb-page-comments-list');
    if (!comments || comments.length === 0) { list.innerHTML = '<p class="gb-page-empty">还没有留言，来说两句吧 👋</p>'; return; }
    var h = '';
    for (var i = comments.length - 1; i >= 0; i--) {
      var c = comments[i];
      h += '<div class="gb-page-comment-item">' +
        '<button class="gb-page-comment-delete" data-index="' + i + '" title="删除此留言">&times;</button>' +
        '<div class="gb-page-comment-meta"><strong>' + escapeHtml(c.name || '匿名') + '</strong> · ' + formatTime(c.time || c.date || '') + '</div>' +
        '<div class="gb-page-comment-body">' + escapeHtml(c.message || '') + '</div>' +
        '</div>';
    }
    list.innerHTML = h;
    list.querySelectorAll('.gb-page-comment-delete').forEach(function(btn) {
      btn.addEventListener('click', function() {
        startDelete(parseInt(this.getAttribute('data-index')));
      });
    });
  }

  function loadAndRender() { fetchComments(renderComments); }

  function showPwd(title, msg) {
    document.getElementById('gb-page-pwd-title').textContent = title || '🔐 输入密码';
    document.getElementById('gb-page-pwd-msg').textContent = msg || '';
    document.getElementById('gb-page-pwd-overlay').style.display = 'flex';
    document.getElementById('gb-page-pwd-input').value = '';
    document.getElementById('gb-page-pwd-input').focus();
  }
  function hidePwd() { document.getElementById('gb-page-pwd-overlay').style.display = 'none'; }

  // ============ Submit ============
  document.getElementById('gb-page-submit-btn').addEventListener('click', function() {
    var msg = document.getElementById('gb-page-input-msg').value.trim();
    if (!msg) { document.getElementById('gb-page-status').textContent = '请输入留言内容'; document.getElementById('gb-page-status').className = 'gb-page-status-error'; return; }
    pendingAction = 'submit';
    showPwd('🔐 发送留言 - 输入密码');
  });

  // ============ Delete ============
  function startDelete(index) {
    if (!COMMENTS_CACHE || index < 0 || index >= COMMENTS_CACHE.length) return;
    pendingAction = { type: 'delete', index: index };
    var c = COMMENTS_CACHE[index];
    showPwd('🔐 删除留言 - 输入密码', '将删除：' + (c.name || '匿名') + ' 的留言（' + formatTime(c.time || '') + '）');
  }

  function doDelete(pwd, index) {
    var token = resolveToken(pwd);
    if (!token) { showPwd('🔐 密码错误', '密码错误，请重试'); pendingAction = null; return; }
    var st = document.getElementById('gb-page-status');
    st.textContent = '⏳ 删除中…'; st.className = '';
    // 直接操作缓存中已获取的最新数据 + SHA
    if (!COMMENTS_CACHE) { st.textContent = '❌ 数据未加载'; st.className = 'gb-page-status-error'; pendingAction = null; return; }
    var comments = COMMENTS_CACHE.slice();
    comments.splice(index, 1);
    saveComments(token, comments, FILE_SHA, '🗑️ 删除留言', function() {
      COMMENTS_CACHE = comments; renderComments(comments);
      st.textContent = '✅ 已删除'; st.className = 'gb-page-status-success';
      pendingAction = null;
    }, function(err) {
      st.textContent = '❌ ' + err; st.className = 'gb-page-status-error'; pendingAction = null;
    });
  }

  // ============ Password confirm ============
  document.getElementById('gb-page-pwd-cancel').addEventListener('click', function() { hidePwd(); pendingAction = null; });
  document.getElementById('gb-page-pwd-confirm').addEventListener('click', function() {
    var pwd = document.getElementById('gb-page-pwd-input').value.trim();
    if (!pwd) { showPwd('🔐 请输入密码', '请输入密码'); return; }
    hidePwd();
    if (pendingAction === 'submit') { doSubmit(pwd); }
    else if (pendingAction && pendingAction.type === 'delete') { doDelete(pwd, pendingAction.index); }
    pendingAction = null;
  });
  document.getElementById('gb-page-pwd-input').addEventListener('keydown', function(e) { if (e.key === 'Enter') document.getElementById('gb-page-pwd-confirm').click(); });

  function doSubmit(pwd) {
    var token = resolveToken(pwd);
    if (!token) { showPwd('🔐 密码错误', '密码错误，请重试'); pendingAction = null; return; }
    var name = document.getElementById('gb-page-input-name').value.trim();
    var msg = document.getElementById('gb-page-input-msg').value.trim();
    var btn = document.getElementById('gb-page-submit-btn'), st = document.getElementById('gb-page-status');
    btn.disabled = true; st.textContent = '⏳ 提交中…'; st.className = '';
    var comments = (COMMENTS_CACHE && COMMENTS_CACHE.length) ? COMMENTS_CACHE.slice() : [];
    comments.push({ name: name || '匿名', message: msg, time: new Date().toISOString() });
    saveComments(token, comments, FILE_SHA, '💬 新增留言 (' + new Date().toISOString().slice(0, 10) + ')', function() {
      COMMENTS_CACHE = comments; renderComments(comments);
      document.getElementById('gb-page-input-msg').value = '';
      document.getElementById('gb-page-input-name').value = '';
      document.getElementById('gb-page-char-count').textContent = '0/500';
      st.textContent = '✅ 留言已发送！'; st.className = 'gb-page-status-success'; btn.disabled = false;
    }, function(err) { st.textContent = '❌ ' + err; st.className = 'gb-page-status-error'; btn.disabled = false; });
  }

  document.getElementById('gb-page-input-msg').addEventListener('input', function() {
    document.getElementById('gb-page-char-count').textContent = this.value.length + '/500';
  });

  loadAndRender();
})();
</script>
