/**
 * guestbook-widget.js
 * 每页底部内嵌留言表单 —— 填写后输入 lcy666 密码即可提交。
 * 所有留言汇入 source/_data/comments.json，在 /guestbook/ 页面统一展示。
 */
(function () {
  'use strict';

  var OWNER = '1whistlerrrr';
  var REPO = '1whistlerrrr.github.io';
  var COMMENTS_PATH = 'source/_data/comments.json';
  var API_URL = 'https://api.github.com/repos/' + OWNER + '/' + REPO + '/contents/' + COMMENTS_PATH;
  var ENCRYPTED_TOKEN = 'CwsJaWEFNFQNUGZXCDISck5xKCIuQ1UGFBo/V3NvBS8YBAUCHDYRZw==';
  var FILE_SHA = null;

  // ==================== CSS ====================
  function injectCSS() {
    if (document.getElementById('gb-widget-css')) return;
    var s = document.createElement('style');
    s.id = 'gb-widget-css';
    s.textContent =
      '#gb-inline-section{margin:40px auto 0;max-width:720px;padding:20px 0;border-top:1px solid #eee;}' +
      '#gb-inline-section .gb-title{font-size:15px;font-weight:600;color:#333;margin-bottom:6px;}' +
      '#gb-inline-section .gb-title a{color:#9FA1FF;font-size:13px;font-weight:400;margin-left:8px;text-decoration:none;}' +
      '#gb-inline-section .gb-title a:hover{text-decoration:underline;}' +
      '#gb-inline-form{display:flex;gap:8px;align-items:flex-start;flex-wrap:wrap;}' +
      '#gb-inline-name{flex:0 0 120px;padding:8px 10px;border:1px solid #ddd;border-radius:8px;font-size:13px;outline:none;box-sizing:border-box;}' +
      '#gb-inline-name:focus{border-color:#9FA1FF;}' +
      '#gb-inline-msg{flex:1;min-width:200px;padding:8px 10px;border:1px solid #ddd;border-radius:8px;font-size:13px;outline:none;resize:none;box-sizing:border-box;font-family:inherit;height:38px;}' +
      '#gb-inline-msg:focus{border-color:#9FA1FF;}' +
      '#gb-inline-submit{padding:8px 18px;background:#9FA1FF;color:#fff;border:none;border-radius:20px;cursor:pointer;font-size:13px;font-weight:500;white-space:nowrap;transition:all .3s;}' +
      '#gb-inline-submit:hover{background:#7c7eff;}' +
      '#gb-inline-submit:disabled{background:#ccc;cursor:not-allowed;}' +
      '#gb-inline-status{font-size:12px;margin-top:6px;min-height:18px;}' +
      '.gb-inline-status-success{color:#2da44e;}.gb-inline-status-error{color:#cf222e;}' +
      '#gb-inline-pwd-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:9999;justify-content:center;align-items:center;}' +
      '#gb-inline-pwd-dialog{background:#fff;border-radius:12px;padding:24px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.2);}' +
      '#gb-inline-pwd-dialog h4{margin:0 0 12px;font-size:16px;color:#333;}' +
      '#gb-inline-pwd-msg{color:#cf222e;font-size:12px;margin:0 0 8px;}' +
      '#gb-inline-pwd-input{padding:8px 12px;border:1px solid #ddd;border-radius:8px;font-size:14px;width:200px;text-align:center;outline:none;}' +
      '#gb-inline-pwd-input:focus{border-color:#9FA1FF;}' +
      '#gb-inline-pwd-actions{margin-top:12px;display:flex;gap:8px;justify-content:center;}' +
      '#gb-inline-pwd-actions button{padding:6px 16px;border-radius:8px;border:1px solid #ddd;background:#fff;cursor:pointer;font-size:13px;}' +
      '#gb-inline-pwd-confirm{background:#9FA1FF!important;color:#fff!important;border-color:#9FA1FF!important;}' +
      '[data-theme="dark"] #gb-inline-section{border-color:#313244;}' +
      '[data-theme="dark"] .gb-title{color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-inline-name,[data-theme="dark"] #gb-inline-msg{background:#313244;border-color:#45475a;color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-inline-pwd-dialog{background:#1e1e2e;}' +
      '[data-theme="dark"] #gb-inline-pwd-dialog h4{color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-inline-pwd-input{background:#313244;border-color:#45475a;color:#cdd6f4;}' +
      '[data-theme="dark"] #gb-inline-pwd-actions button{background:#313244;border-color:#45475a;color:#cdd6f4;}';
    document.head.appendChild(s);
  }

  // ==================== Token ====================
  function decryptToken(encB64, pwd) {
    try {
      var b = atob(encB64), bytes = new Uint8Array(b.length);
      for (var i = 0; i < b.length; i++) bytes[i] = b.charCodeAt(i);
      var key = pwd.repeat(Math.ceil(bytes.length / pwd.length)).slice(0, bytes.length);
      var r = new Uint8Array(bytes.length);
      for (var i = 0; i < bytes.length; i++) r[i] = bytes[i] ^ key.charCodeAt(i);
      return String.fromCharCode.apply(null, r);
    } catch (e) { return ''; }
  }

  function setCachedToken(t) { try { localStorage.setItem('gh_mindmap_token', t); } catch (e) {} }

  function resolveToken(pwd) {
    if (!pwd) return null;
    var tok = decryptToken(ENCRYPTED_TOKEN, pwd);
    if (!tok || (!tok.startsWith('ghp_') && !tok.startsWith('github_pat_'))) return null;
    setCachedToken(tok);
    return tok;
  }

  // ==================== GitHub API ====================
  function getFileSha(token, cb, errCb) {
    var x = new XMLHttpRequest();
    x.open('GET', API_URL, true);
    x.setRequestHeader('Authorization', 'Bearer ' + token);
    x.setRequestHeader('Accept', 'application/vnd.github+json');
    x.onload = function () {
      if (x.status === 200) {
        var d = JSON.parse(x.responseText);
        FILE_SHA = d.sha; cb(FILE_SHA);
      } else if (x.status === 404) {
        FILE_SHA = null; cb(null);
      } else {
        errCb('获取文件失败 (' + x.status + ')');
      }
    };
    x.onerror = function () { errCb('网络错误'); };
    x.send();
  }

  function fetchAndSave(token, name, msg, cb, errCb) {
    // 先拉取最新 comments
    var rawUrl = 'https://raw.githubusercontent.com/' + OWNER + '/' + REPO + '/main/' + COMMENTS_PATH + '?t=' + Date.now();
    var x1 = new XMLHttpRequest();
    x1.open('GET', rawUrl, true);
    x1.onload = function () {
      var comments = [];
      if (x1.status === 200) { try { comments = JSON.parse(x1.responseText); } catch (e) {} }
      comments.push({ name: name, message: msg, time: new Date().toISOString() });
      // 获取 SHA
      getFileSha(token, function (sha) {
        var x2 = new XMLHttpRequest();
        x2.open('PUT', API_URL, true);
        x2.setRequestHeader('Authorization', 'Bearer ' + token);
        x2.setRequestHeader('Content-Type', 'application/json');
        x2.setRequestHeader('Accept', 'application/vnd.github+json');
        var body = { message: '💬 新增留言 (' + new Date().toISOString().slice(0, 10) + ')',
          content: btoa(unescape(encodeURIComponent(JSON.stringify(comments, null, 2)))) };
        if (sha) body.sha = sha;
        x2.onload = function () {
          if (x2.status === 200 || x2.status === 201) { cb(); }
          else { errCb('提交失败 (' + x2.status + ')'); }
        };
        x2.onerror = function () { errCb('网络错误'); };
        x2.send(JSON.stringify(body));
      }, errCb);
    };
    x1.onerror = function () { errCb('网络错误'); };
    x1.send();
  }

  // ==================== UI ====================
  function buildWidget() {
    if (document.getElementById('gb-inline-section')) return;

    var section = document.createElement('div');
    section.id = 'gb-inline-section';
    section.innerHTML =
      '<div class="gb-title">💬 留言 <a href="/guestbook/">查看全部 →</a></div>' +
      '<div id="gb-inline-form">' +
      '  <input type="text" id="gb-inline-name" placeholder="昵称" maxlength="20" />' +
      '  <input type="text" id="gb-inline-msg" placeholder="写留言…" maxlength="500" />' +
      '  <button id="gb-inline-submit">发送</button>' +
      '</div>' +
      '<p id="gb-inline-status"></p>' +
      '<div id="gb-inline-pwd-overlay">' +
      '  <div id="gb-inline-pwd-dialog">' +
      '    <h4>🔐 输入密码</h4>' +
      '    <p id="gb-inline-pwd-msg"></p>' +
      '    <input type="password" id="gb-inline-pwd-input" placeholder="请输入密码" />' +
      '    <div id="gb-inline-pwd-actions">' +
      '      <button id="gb-inline-pwd-cancel">取消</button>' +
      '      <button id="gb-inline-pwd-confirm">确认提交</button>' +
      '    </div>' +
      '  </div>' +
      '</div>';

    // 插入到文章内容区域底部
    var container = document.querySelector('.layout') || document.querySelector('main') || document.querySelector('.post-content') || document.body;
    // 找到合适的插入点：文章的末尾
    var postContent = document.querySelector('.post-content') || document.querySelector('#article-container') || document.querySelector('.post-content-wrap');
    if (postContent) {
      postContent.appendChild(section);
    } else {
      // fallback: 插在 body 末尾但 footer 之前
      var footer = document.querySelector('footer');
      if (footer) {
        footer.parentNode.insertBefore(section, footer);
      } else {
        document.body.appendChild(section);
      }
    }

    bindEvents();
  }

  function bindEvents() {
    document.getElementById('gb-inline-submit').addEventListener('click', function () {
      var msg = document.getElementById('gb-inline-msg').value.trim();
      if (!msg) {
        showStatus('请输入留言内容', 'error');
        return;
      }
      showPwdDialog('');
    });

    document.getElementById('gb-inline-pwd-cancel').addEventListener('click', hidePwdDialog);
    document.getElementById('gb-inline-pwd-confirm').addEventListener('click', function () {
      var pwd = document.getElementById('gb-inline-pwd-input').value.trim();
      if (!pwd) { showPwdDialog('请输入密码'); return; }
      hidePwdDialog();
      doSubmit(pwd);
    });
    document.getElementById('gb-inline-pwd-input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') document.getElementById('gb-inline-pwd-confirm').click();
    });
    document.getElementById('gb-inline-msg').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') document.getElementById('gb-inline-submit').click();
    });
  }

  function showStatus(msg, type) {
    var el = document.getElementById('gb-inline-status');
    el.textContent = msg;
    el.className = type === 'success' ? 'gb-inline-status-success' : (type === 'error' ? 'gb-inline-status-error' : '');
  }

  function showPwdDialog(msg) {
    document.getElementById('gb-inline-pwd-overlay').style.display = 'flex';
    document.getElementById('gb-inline-pwd-msg').textContent = msg || '';
    document.getElementById('gb-inline-pwd-input').value = '';
    document.getElementById('gb-inline-pwd-input').focus();
  }

  function hidePwdDialog() {
    document.getElementById('gb-inline-pwd-overlay').style.display = 'none';
  }

  function doSubmit(pwd) {
    var token = resolveToken(pwd);
    if (!token) { showPwdDialog('密码错误，请重试'); return; }

    var name = document.getElementById('gb-inline-name').value.trim();
    var msg = document.getElementById('gb-inline-msg').value.trim();
    var btn = document.getElementById('gb-inline-submit');
    btn.disabled = true;
    showStatus('⏳ 提交中…', '');

    fetchAndSave(token, name || '匿名', msg, function () {
      document.getElementById('gb-inline-msg').value = '';
      document.getElementById('gb-inline-name').value = '';
      showStatus('✅ 留言已发送！前往 <a href="/guestbook/" style="color:#9FA1FF;">留言板</a> 查看全部', 'success');
      btn.disabled = false;
    }, function (err) {
      showStatus('❌ ' + err, 'error');
      btn.disabled = false;
    });
  }

  // ==================== Init ====================
  injectCSS();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildWidget);
  } else {
    buildWidget();
  }
})();
