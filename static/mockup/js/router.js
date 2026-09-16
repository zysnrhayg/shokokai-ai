(function () {
  var VIEW_BY_ROUTE = {
    home: 'view-home',
    'ai-input': 'view-entry',
    'manual-input': 'view-entry',
    'expert-import': 'view-entry',
    reports: 'view-reports',
    'ai-proposal': 'view-ai-proposal',
    monthly: 'view-monthly',
    accounts: 'view-accounts',
    knowledge: 'view-knowledge',
    'knowledge-search': 'view-knowledge-search',
  };

  function showLoginError(message) {
    var errorEl = document.getElementById('login-error');
    if (!errorEl) return;
    errorEl.textContent = message || '⚠ 入力内容をご確認ください';
    errorEl.style.display = '';
  }

  function showMfaError(message) {
    var errorEl = document.getElementById('mfa-error');
    if (!errorEl) return;
    errorEl.textContent = message || '⚠ 確認コードが正しくありません';
    errorEl.style.display = '';
  }

  function parseLoginResponse(res) {
    if (typeof res !== 'string') return res;
    var text = res.trim();
    if (text === 'OK') return { OK: '#home' };
    try {
      return JSON.parse(text);
    } catch (err) {
      if (text.indexOf('OK') !== -1) return { OK: '#home' };
      return null;
    }
  }

  function postJson(url, body) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    }).then(function (response) {
      return response.text().then(function (text) {
        return { ok: response.ok, text: text, data: parseLoginResponse(text) };
      });
    });
  }

  function fillPrefectureSelect(prefectures) {
    var select = document.getElementById('login-prefecture');
    if (!select) return;
    var previous = select.value || (typeof localStorage !== 'undefined' ? localStorage.getItem('prefecture_code') : '') || '';
    select.innerHTML = '';
    (prefectures || []).forEach(function (row) {
      var option = document.createElement('option');
      option.value = row.prefecture_code || '';
      option.textContent = row.name || row.short_name || row.prefecture_code || '';
      select.appendChild(option);
    });
    if (previous && select.querySelector('option[value="' + previous + '"]')) {
      select.value = previous;
    }
  }

  function fillLoginNotices(notices) {
    var box = document.getElementById('login-notice-items');
    if (!box) return;
    box.innerHTML = '';
    (notices || []).forEach(function (row) {
      var item = document.createElement('div');
      item.className = 'login-notice__item';
      item.textContent = row.content || '';
      if (item.textContent) box.appendChild(item);
    });
  }

  function initLoginPage() {
    if (window.__loginInitStarted) return;
    window.__loginInitStarted = true;
    postJson('./logininitapi.do', {}).then(function (result) {
      var data = result.data || {};
      fillPrefectureSelect(data.prefectures);
      fillLoginNotices(data.notices);
    }).catch(function () {
      window.__loginInitStarted = false;
    });
  }

  function markLoggedIn(data, userid) {
    window.__IS_LOGGED_IN = true;
    var username = (data && data.username) || userid;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('userid', userid);
      if (username) localStorage.setItem('username', username);
      var pref = (data && (data.prefecturecode || data.prefecture_code)) || '';
      var shokokai = (data && (data.shokokaicd || data.shokokai_cd)) || '';
      if (pref) localStorage.setItem('prefecture_code', pref);
      if (shokokai) localStorage.setItem('shokokai_cd', shokokai);
    }
    var userInfo = document.querySelector('.user-info');
    if (userInfo && userid) {
      userInfo.textContent = userid + (username ? '：' + username : '');
    }
    var roleEl = document.getElementById('org-role-select');
    if (roleEl) {
      var loginPref = (data && (data.prefecturecode || data.prefecture_code))
        || (typeof localStorage !== 'undefined' && localStorage.getItem('prefecture_code'))
        || '';
      var loginSho = (data && (data.shokokaicd || data.shokokai_cd))
        || (typeof localStorage !== 'undefined' && localStorage.getItem('shokokai_cd'))
        || '';
      var nextRole = 'shokokai';
      if (loginPref === '00') nextRole = 'national';
      else if (loginSho === '0021') nextRole = 'pref';
      if (roleEl.value !== nextRole) {
        roleEl.value = nextRole;
        roleEl.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  }

  function route() {

    var hasHash = typeof location.hash === 'string' && location.hash.length > 0;
    if (!hasHash) {
      location.hash = '#login';
      return;
    }
    var key = location.hash.slice(1) || 'login';
    var authPages = { login: true, 'verify-2fa': true };
    if (!window.__IS_LOGGED_IN && !authPages[key]) {
      location.hash = '#login';
      return;
    }

    var appShell = document.getElementById('app-shell');
    var loginView = document.getElementById('view-login');
    var mfaView = document.getElementById('view-verify-2fa');
    if (key === 'login') {
      if (appShell) appShell.style.display = 'none';
      if (mfaView) mfaView.style.display = 'none';
      if (loginView) loginView.style.display = 'block';
      initLoginPage();
      return;
    }
    if (key === 'verify-2fa') {
      if (appShell) appShell.style.display = 'none';
      if (loginView) loginView.style.display = 'none';
      if (mfaView) mfaView.style.display = 'block';

      var otpBoxes = mfaView ? mfaView.querySelectorAll('.login-otp-box') : [];
      otpBoxes.forEach(function (b) { b.value = ''; });
      var otpHidden = document.getElementById('login-otp-hidden');
      if (otpHidden) otpHidden.value = '';
      var mfaErrorEl = document.getElementById('mfa-error');
      if (mfaErrorEl) mfaErrorEl.style.display = 'none';
      if (otpBoxes[0]) otpBoxes[0].focus();
      return;
    }
    if (appShell) appShell.style.display = 'block';
    if (loginView) loginView.style.display = 'none';
    if (mfaView) mfaView.style.display = 'none';
    if (typeof window.syncTopBarHeight === 'function') window.syncTopBarHeight();

    var viewId = VIEW_BY_ROUTE[key] || 'view-home';
    if (!VIEW_BY_ROUTE[key]) key = 'home';

    document.querySelectorAll('#main-mount > .app-view').forEach(function (el) {
      el.classList.toggle('active', el.id === viewId);
    });

    document.querySelectorAll('.sidebar .nav-item[data-route]').forEach(function (el) {
      el.classList.toggle('active', el.dataset.route === key);
    });

    var backBtn = document.getElementById('app-back-btn');
    if (backBtn) backBtn.style.display = (key === 'home') ? 'none' : '';

    if (viewId === 'view-entry' && typeof applyEntryScreen === 'function') {
      applyEntryScreen(key);
    } else if (key === 'reports') {
      document.getElementById('app-title').textContent = '報告書を見る';
      document.getElementById('app-subtitle').textContent = '受付票と各種報告書を見れます';

      if (typeof window.__renderReports === 'function') window.__renderReports();

      requestAnimationFrame(() => {
        alignCardBottomToManualInput(document.querySelector('#view-reports .card.card--fill'), true);
        syncReportsMonthlyFilterHeaderHeight();
      });
    } else if (key === 'ai-proposal') {
      document.getElementById('app-title').textContent = 'AIと一緒に考える';
      document.getElementById('app-subtitle').textContent = '相談内容をもとに、蓄積されたナレッジからAIが最適な支援提案を提示します';

      if (typeof window.__renderAiProposal === 'function') window.__renderAiProposal();
    } else if (key === 'accounts') {
      document.getElementById('app-title').textContent = 'アカウント管理';
      document.getElementById('app-subtitle').textContent = 'システムにログインするアカウントを管理できます';

      if (typeof window.__renderAccounts === 'function') window.__renderAccounts();
      requestAnimationFrame(() => {
        alignCardBottomToManualInput(document.querySelector('#accounts-filter-card'), true);
        syncReportsMonthlyFilterHeaderHeight();
      });
    } else if (key === 'monthly') {
      document.getElementById('app-title').textContent = '実績確認・帳票出力';
      document.getElementById('app-subtitle').textContent = '月次・年次の実績確認と帳票を出力できます';

      if (typeof window.__renderMonthly === 'function') window.__renderMonthly();

      requestAnimationFrame(() => {
        syncReportsMonthlyFilterHeaderHeight();
      });
    } else if (key === 'knowledge') {
      document.getElementById('app-title').textContent = 'ナレッジ管理';
      document.getElementById('app-subtitle').textContent = '過去の相談・報告データや規定等ナレッジを管理します';
      if (typeof window.__renderKnowledge === 'function') window.__renderKnowledge();
    } else if (key === 'knowledge-search') {
      document.getElementById('app-title').textContent = 'ナレッジを検索する';
      document.getElementById('app-subtitle').textContent = 'キーワードで蓄積されたナレッジベースを検索します';
      if (typeof window.__renderKnowledgeSearch === 'function') window.__renderKnowledgeSearch();
    } else if (key === 'home') {
      document.getElementById('app-title').textContent = 'ホーム';
      document.getElementById('app-subtitle').textContent = '事業環境変化対応型支援事業';
      if (typeof window.__renderHomeForRole === 'function') {
        var roleEl = document.getElementById('org-role-select');
        window.__renderHomeForRole(roleEl ? roleEl.value : 'shokokai');
      }
    }
  }

  var loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var prefectureEl = document.getElementById('login-prefecture');
      var userIdEl = document.getElementById('login-user-id');
      var passwordEl = document.getElementById('login-password');
      var rememberEl = document.getElementById('login-remember');
      var errorEl = document.getElementById('login-error');
      var prefecture = prefectureEl ? prefectureEl.value.trim() : '';
      var userid = userIdEl ? userIdEl.value.trim() : '';
      var pwd = passwordEl ? passwordEl.value.trim() : '';
      var remember = rememberEl && rememberEl.checked;
      if (!prefecture || !userid || !pwd) {
        showLoginError('⚠ 入力内容をご確認ください');
        return;
      }
      if (errorEl) errorEl.style.display = 'none';
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem('prefecture_code', prefecture);
      }

      postJson('./loginapi.do', {
        prefecturecode: prefecture,
        userid: userid,
        password: pwd,
        remember: remember ? 'true' : 'false'
      }).then(function (result) {
        var data = result.data || {};
        if (result.ok && data.need_mfa) {
          location.hash = '#verify-2fa';
          return;
        }
        var success = result.ok && data && (data.OK || data.WF_RUNRESULT === '1');
        if (success && !data.i && !data.e) {
          markLoggedIn(data, userid);
          location.hash = '#home';
          return;
        }
        var msg = data.i || data.e || data.c || '⚠ 入力内容をご確認ください';
        showLoginError(msg);
      }).catch(function () {
        showLoginError('⚠ ログインに失敗しました。しばらくしてから再度お試しください');
      });
    });
  }

  var mfaForm = document.getElementById('mfa-form');
  if (mfaForm) {
    mfaForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var hiddenEl = document.getElementById('login-otp-hidden');
      var errorEl = document.getElementById('mfa-error');
      var boxes = document.querySelectorAll('#login-otp-row .login-otp-box');
      var fromBoxes = Array.prototype.map.call(boxes, function (b) { return (b.value || '').replace(/\D/g, ''); }).join('');
      var code = fromBoxes || (hiddenEl ? hiddenEl.value : '');
      if (errorEl) errorEl.style.display = 'none';
      postJson('./verify2faapi.do', { code: code, rememberdevice: 'false' }).then(function (result) {
        var data = result.data || {};
        var success = result.ok && data && (data.OK || data.WF_RUNRESULT === '1') && !data.i && !data.e;
        if (success) {
          var userid = (typeof localStorage !== 'undefined' && localStorage.getItem('userid')) || '';
          markLoggedIn(data, userid);
          location.hash = '#home';
          return;
        }
        showMfaError(data.i || data.e || '⚠ 確認コードが正しくありません');
      }).catch(function () {
        showMfaError('⚠ 確認コードが正しくありません');
      });
    });
  }

  window.addEventListener('hashchange', route);
  route();
})();
