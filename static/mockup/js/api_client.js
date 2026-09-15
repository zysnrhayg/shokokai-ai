/** Shared POST JSON client for mockup SPA ↔ *.do APIs */
(function (global) {
  function getCsrfToken() {
    var el = document.querySelector('input[name="csrf_token"]');
    return el ? el.value : '';
  }

  function postApi(url, body) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify(body || {}),
    }).then(function (response) {
      return response.text().then(function (text) {
        var data = null;
        try {
          data = text ? JSON.parse(text) : {};
        } catch (e) {
          data = { e: text };
        }
        if (data && data.r && !data.dragB && !data.account && !data.useraccountid && !data.proposals && !data.themes && !data.industries) {
          data.e = data.e || 'セッションが切れました。再ログインしてください';
        }
        if (response.status === 403) {
          data = data || {};
          data.e = data.e || data.message || 'CSRFエラーです。ページを再読み込み（Ctrl+F5）してから再ログインしてください';
        }
        return { ok: response.ok, status: response.status, data: data || {} };
      });
    });
  }

  function orgContext() {
    var pref = (typeof localStorage !== 'undefined' && localStorage.getItem('prefecture_code')) || '';
    var shokokai = (typeof localStorage !== 'undefined' && localStorage.getItem('shokokai_cd')) || '';
    // Empty values let the server fall back to session PREFECTURE_CODE / SHOKOKAI_CD.
    // Do not hardcode 00/0021 — that filters out most seed trn_report rows.
    return {
      prefecturecode: pref,
      shokokaicd: shokokai,
    };
  }

  global.ApiClient = {
    post: postApi,
    getCsrfToken: getCsrfToken,
    orgContext: orgContext,
  };
})(typeof window !== 'undefined' ? window : this);
