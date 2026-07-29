/**
 * guestbook-widget.js
 * 浮动留言板 —— 每个页面右下角显示"💬 留言"按钮，点击打开留言弹窗。
 * 数据存储在 source/_data/comments.json，通过 GitHub API 读写。
 *
 * 密码：lcy666（与 mindmap 共享 Token 加密方案）
 */
(function () {
  'use strict';

  var OWNER = '1whistlerrrr';
  var REPO = '1whistlerrrr.github.io';
  var COMMENTS_PATH = 'source/_data/comments.json';
  var RAW_URL = 'https://raw.githubusercontent.com/' + OWNER + '/' + REPO + '/main/' + COMMENTS_PATH;
  var API_URL = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + COMMENTS_PATH;
  // 与 mindmap 共享的加密 Token（XOR + base64，密码 lcy666）
  var ENCRYPTED_TOKEN = 'CwsJaWEFNFQNUGZXCDISck5xKCIuQ1UGFBo/V3NvBS8YBAUCHDYRZw==';
  var COMMENTS_CACHE = null;
  var FILE_SHA = null;

  // ==================== CSS (self-injected) ====================
  function injectCSS() {
    if (document.getElementById('gb-widget-css')) return;
    var style = document.createElement('style');
    style.id = 'gb-widget-css';
    style.textContent =
      /* float button */
      '#gb-float-btn{position:fixed;bottom:80px;right:24px;width:48px;height:48px;' +
      'border-radius:50%;background:#9FA1FF;color:#fff;border:none;font-size:22px;' +
      'cursor:pointer;z-index:9998;box-shadow:0 4px 16px rgba(159,161,255,.4);' +
      'transition:transform .2s,box-shadow .2s;line-height:48px;text-align:center;padding:0;}' +
      '#gb-float-btn:hover{transform:scale(1.1);box-shadow:0 6px 24px rgba(159,161,255,.6);}' +
      /* overlay & dialog */
      '#gb-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;' +
      'background:rgba(0,0,0,.5);z-index:9999;justify-content:center;align-items:center;}' +
      '#gb-dialog{background:#fff;border-radius:16px;max-width:520px;width:92%;' +
      'max-height:80vh;display:flex;flex-direction:column;box-shadow:0 16px 48px rgba(0,0,0,.25);}' +
      '.gb-header{display:flex;justify-content:space-between;align-items:center;' +
      'padding:16px 20px;border-bottom:1px solid #eee;}' +
      '.gb-header h3{margin:0;font-size:18px;color:#333;}' +
      '#gb-close-btn{background:none;border:none;font-size:24px;cursor:pointer;color:#999;padding:0 4px;}' +
      '#gb-close-btn:hover{color:#333;}' +
      /* comments list */
      '#gb-comments-list{flex:1;overflow-y:auto;padding:16px 20px;min-height:120px;max-height:300px;}' +
      '.gb-loading,.gb-empty{text-align:center;color:#999;padding:24px 0;font-size:14px;}' +
      '.gb-comment-item{padding:10px 0;border-bottom:1px solid #f5f5f5;}' +
      '.gb-comment-item:last-child{border-bottom:none;}' +
      '.gb-comment-meta{font-size:12px;color:#888;margin-bottom:4px;}' +
      '.gb-comment-body{font-size:14px;color:#333;line-height:1.6;word-break:break-word;}' +
      /* form */
      '.gb-form{padding:12px 20px 16px;border-top:1px solid #eee;}' +
      '#gb-input-name{width:100%;padding:8px 12px;border:1px solid #ddd;border-radius:8px;' +
      'font-size:13px;margin-bottom:8px;box-sizing:border-box;outline:none;}' +
      '#gb-input-name:focus{border-color:#9FA1FF;}' +
      '#gb-input-msg{width:100%;padding:8px 12px;border:1px solid #ddd;border-radius:8px;' +
      'font-size:13px;resize:vertical;box-sizing:border-box;outline:none;font-family:inherit;}' +
      '#gb-input-msg:focus{border-color:#9FA1FF;}' +
      '.gb-form-row{display:flex;justify-content:space-between;align-items:center;margin-top:8px;}' +
      '#gb-char-count{font-size:12px;color:#999;}' +
      '.gb-submit-btn{padding:8px 20px;background:#9FA1FF;color:#fff;border:none;' +
      'border-radius:20px;cursor:pointer;font-size:13px;font-weight:500;transition:all .3s;}' +
      '.gb-submit-btn:hover{background:#7c7eff;}' +
      '.gb-submit-btn:disabled{background:#ccc;cursor:not-allowed;}' +
      '#gb-status{font-size:12px;margin:6px 0 0;min-height:18px;}' +
      '.gb-status-success{color:#2da44e;}.gb-status-error{color:#cf222e;}' +
      /* password dialog */
      '#gb-pwd-overlay{display:none;position:absolute;top:0;left:0;right:0;bottom:0;' +
      'background:rgba(255,255,255,.95);border-radius:16px;justify-content:center;align-items:center;z-index:10;}' +
      '.gb-pwd-dialog{text-align:center;padding:24px;}' +
      '.gb-pwd-dialog h4{margin:0 0 12px;font-size:16px;color:#333;}' +
      '#gb-pwd-input{padding:8px 12px;border:1px solid #ddd;border-radius:8px;' +
      'font-size:14px;width:200px;text-align:center;outline:none;}' +
      '#gb-pwd-input:focus{border-color:#9FA1FF;}' +
      '.gb-pwd-actions{margin-top:12px;display:flex;gap:8px;justify-content:center;}' +
      '.gb-pwd-actions button{padding:6px 16px;border-radius:8px;border:1px solid #ddd;' +
      'background:#fff;cursor:pointer;font-size:13px;}' +
      '.gb-btn-primary{background:#9FA1FF!important;color:#fff!important;border-color:#9FA1FF!important;}' +
      /* dark mode */
      '[data-theme="dark"] #gb-dialog{background:#1e1e2e;}' +
      '[data-theme="dark"] .gb-header{border-color:#313244;}' +
      '[data-theme="dark"] .gb-header h3{color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-close-btn{color:#6c7086;}' +
      '[data-theme="dark"] #gb-close-btn:hover{color:#cdd6f4;}' +
      '[data-theme="dark"] .gb-comment-item{border-color:#313244;}' +
      '[data-theme="dark"] .gb-comment-meta{color:#6c7086;}' +
      '[data-theme="dark"] .gb-comment-body{color:#cdd6f4;}' +
      '[data-theme="dark"] .gb-form{border-color:#313244;}' +
      '[data-theme="dark"] #gb-input-name,[data-theme="dark"] #gb-input-msg{background:#313244;border-color:#45475a;color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-pwd-overlay{background:rgba(30,30,46,.97);}' +
      '[data-theme="dark"] .gb-pwd-dialog h4{color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-pwd-input{background:#313244;border-color:#45475a;color:#cdd6f4;}' +
      '[data-theme="dark"] .gb-pwd-actions button{background:#313244;border-color:#45475a;color:#cdd6f4;}';
    document.head.appendChild(style);
  }

  // ==================== Token / Auth ====================
  function decryptToken(encB64, password) {
    try {
      var binary = atob(encB64);
      var bytes = new Uint8Array(binary.length);
      for (var i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      var key = password.repeat(Math.ceil(bytes.length / password.length)).slice(0, bytes.length);
      var result = new Uint8Array(bytes.length);
      for (var i = 0; i < bytes.length; i++) result[i] = bytes[i] ^ key.charCodeAt(i);
      return String.fromCharCode.apply(null, result);
    } catch (e) { return ''; }
  }

  function getCachedToken() {
    try { return localStorage.getItem('gh_mindmap_token') || ''; } catch (e) { return ''; }
  }
  function setCachedToken(t) {
    try { localStorage.setItem('gh_mindmap_token', t); } catch (e) { /* ignore */ }
  }

  function resolveToken(password) {
    if (ENCRYPTED_TOKEN && password && password.length < 50) {
      var token = decryptToken(ENCRYPTED_TOKEN, password);
      if (!token || (!token.startsWith('ghp_') && !token.startsWith('github_pat_'))) return null;
      setCachedToken(token);
      return token;
    }
    return getCachedToken();
  }

  // ==================== GitHub API ====================
  function fetchComments(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', RAW_URL + '?t=' + Date.now(), true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        try { COMMENTS_CACHE = JSON.parse(xhr.responseText); } catch (e) { COMMENTS_CACHE = []; }
      } else {
        COMMENTS_CACHE = [];
      }
      callback(COMMENTS_CACHE);
    };
    xhr.onerror = function () { callback(COMMENTS_CACHE || []); };
    xhr.send();
  }

  function getFileSha(token, callback, onError) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', API_URL, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token);
    xhr.setRequestHeader('Accept', 'application/vnd.github+json');
    xhr.onload = function () {
      if (xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        FILE_SHA = data.sha;
        callback(FILE_SHA);
      } else if (xhr.status === 404) {
        FILE_SHA = null;
        callback(null);
      } else {
        onError('获取文件信息失败 (' + xhr.status + ')');
      }
    };
    xhr.onerror = function () { onError('网络错误'); };
    xhr.send();
  }

  function saveComments(token, comments, sha, callback, onError) {
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', API_URL, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/vnd.github+json');
    var body = {
      message: '💬 新增留言 (' + new Date().toISOString().slice(0, 10) + ')',
      content: btoa(unescape(encodeURIComponent(JSON.stringify(comments, null, 2))))
    };
    if (sha) body.sha = sha;
    xhr.onload = function () {
      if (xhr.status === 200 || xhr.status === 201) {
        var data = JSON.parse(xhr.responseText);
        FILE_SHA = data.content ? data.content.sha : sha;
        callback();
      } else {
        onError('提交失败 (' + xhr.status + ')');
      }
    };
    xhr.onerror = function () { onError('网络错误'); };
    xhr.send(JSON.stringify(body));
  }

  // ==================== UI ====================
  function createWidget() {
    if (document.getElementById('guestbook-widget-root')) return;

    var root = document.createElement('div');
    root.id = 'guestbook-widget-root';
    root.innerHTML =
      '<button id="gb-float-btn" title="留言板">💬</button>' +
      '<div id="gb-overlay">' +
      '  <div id="gb-dialog">' +
      '    <div class="gb-header">' +
      '      <h3>💬 留言板</h3>' +
      '      <button id="gb-close-btn">&times;</button>' +
      '    </div>' +
      '    <div id="gb-comments-list"><p class="gb-loading">加载中…</p></div>' +
      '    <div class="gb-form">' +
      '      <input type="text" id="gb-input-name" placeholder="昵称（选填）" maxlength="30" />' +
      '      <textarea id="gb-input-msg" placeholder="写留言…" rows="3" maxlength="500"></textarea>' +
      '      <div class="gb-form-row">' +
      '        <span id="gb-char-count">0/500</span>' +
      '        <button id="gb-submit-btn" class="gb-submit-btn">发送留言</button>' +
      '      </div>' +
      '      <p id="gb-status"></p>' +
      '    </div>' +
      '    <div id="gb-pwd-overlay">' +
      '      <div class="gb-pwd-dialog">' +
      '        <h4>🔐 输入密码</h4>' +
      '        <p id="gb-pwd-msg" style="color:#cf222e;font-size:12px;margin:0 0 8px;"></p>' +
      '        <input type="password" id="gb-pwd-input" placeholder="请输入密码" />' +
      '        <div class="gb-pwd-actions">' +
      '          <button id="gb-pwd-cancel">取消</button>' +
      '          <button id="gb-pwd-confirm" class="gb-btn-primary">确认</button>' +
      '        </div>' +
      '      </div>' +
      '    </div>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(root);
    bindEvents();
  }

  function bindEvents() {
    var floatBtn = document.getElementById('gb-float-btn');
    var overlay = document.getElementById('gb-overlay');
    var closeBtn = document.getElementById('gb-close-btn');
    var submitBtn = document.getElementById('gb-submit-btn');
    var msgInput = document.getElementById('gb-input-msg');
    var charCount = document.getElementById('gb-char-count');
    var pwdOverlay = document.getElementById('gb-pwd-overlay');
    var pwdCancel = document.getElementById('gb-pwd-cancel');
    var pwdConfirm = document.getElementById('gb-pwd-confirm');
    var pwdInputEl = document.getElementById('gb-pwd-input');

    floatBtn.addEventListener('click', openGuestbook);
    closeBtn.addEventListener('click', closeGuestbook);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeGuestbook(); });

    msgInput.addEventListener('input', function () {
      charCount.textContent = msgInput.value.length + '/500';
    });

    submitBtn.addEventListener('click', handleSubmit);

    pwdCancel.addEventListener('click', function () { pwdOverlay.style.display = 'none'; });
    pwdConfirm.addEventListener('click', function () {
      var pwd = pwdInputEl.value.trim();
      if (!pwd) { showPwdError('请输入密码'); return; }
      pwdOverlay.style.display = 'none';
      doSubmit(pwd);
    });
    pwdInputEl.addEventListener('keydown', function (e) { if (e.key === 'Enter') pwdConfirm.click(); });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.style.display === 'flex') closeGuestbook();
    });
  }

  function openGuestbook() {
    document.getElementById('gb-overlay').style.display = 'flex';
    document.getElementById('gb-status').textContent = '';
    document.getElementById('gb-status').className = '';
    loadAndRender();
  }

  function closeGuestbook() {
    document.getElementById('gb-overlay').style.display = 'none';
  }

  function showPwdError(msg) {
    document.getElementById('gb-pwd-msg').textContent = msg;
    document.getElementById('gb-pwd-overlay').style.display = 'flex';
    document.getElementById('gb-pwd-input').value = '';
    document.getElementById('gb-pwd-input').focus();
  }

  // ==================== Comment rendering ====================
  function formatTime(isoStr) {
    var d = new Date(isoStr);
    var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + ' ' +
      pad(d.getHours()) + ':' + pad(d.getMinutes());
  }

  function renderComments(comments) {
    var list = document.getElementById('gb-comments-list');
    if (!comments || comments.length === 0) {
      list.innerHTML = '<p class="gb-empty">还没有留言，来说两句吧 👋</p>';
      return;
    }
    var html = '';
    for (var i = comments.length - 1; i >= 0; i--) {
      var c = comments[i];
      var name = escapeHtml(c.name || '匿名');
      var msg = escapeHtml(c.message || '');
      var time = formatTime(c.time || c.date || '');
      html +=
        '<div class="gb-comment-item">' +
        '  <div class="gb-comment-meta"><strong>' + name + '</strong> · ' + time + '</div>' +
        '  <div class="gb-comment-body">' + msg + '</div>' +
        '</div>';
    }
    list.innerHTML = html;
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function loadAndRender() {
    fetchComments(function (comments) {
      renderComments(comments);
    });
  }

  // ==================== Submit ====================
  function handleSubmit() {
    var msg = document.getElementById('gb-input-msg').value.trim();
    if (!msg) {
      document.getElementById('gb-status').textContent = '请输入留言内容';
      document.getElementById('gb-status').className = 'gb-status-error';
      return;
    }
    var cached = getCachedToken();
    if (cached) {
      doSubmit(null);
      return;
    }
    document.getElementById('gb-pwd-overlay').style.display = 'flex';
    document.getElementById('gb-pwd-input').value = '';
    document.getElementById('gb-pwd-msg').textContent = '';
    document.getElementById('gb-pwd-input').focus();
  }

  function doSubmit(password) {
    var token = resolveToken(password);
    if (!token) {
      showPwdError('密码错误，请重试');
      return;
    }
    var name = document.getElementById('gb-input-name').value.trim();
    var msg = document.getElementById('gb-input-msg').value.trim();
    var submitBtn = document.getElementById('gb-submit-btn');
    var statusEl = document.getElementById('gb-status');

    submitBtn.disabled = true;
    statusEl.textContent = '⏳ 提交中…';
    statusEl.className = '';

    getFileSha(token, function (sha) {
      var comments = (COMMENTS_CACHE && COMMENTS_CACHE.length) ? COMMENTS_CACHE.slice() : [];
      comments.push({ name: name || '匿名', message: msg, time: new Date().toISOString() });
      saveComments(token, comments, sha, function () {
        COMMENTS_CACHE = comments;
        renderComments(comments);
        document.getElementById('gb-input-msg').value = '';
        document.getElementById('gb-input-name').value = '';
        document.getElementById('gb-char-count').textContent = '0/500';
        statusEl.textContent = '✅ 留言已发送！';
        statusEl.className = 'gb-status-success';
        submitBtn.disabled = false;
      }, function (err) {
        statusEl.textContent = '❌ ' + err;
        statusEl.className = 'gb-status-error';
        submitBtn.disabled = false;
      });
    }, function (err) {
      statusEl.textContent = '❌ ' + err;
      statusEl.className = 'gb-status-error';
      submitBtn.disabled = false;
    });
  }

  // ==================== Init ====================
  injectCSS();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }
})();
