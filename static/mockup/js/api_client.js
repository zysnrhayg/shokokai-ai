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
        if (data && data.r && !data.dragB && !data.account && !data.useraccountid && !data.proposals && !data.themes && !data.industries && !data.heatmap && !data.monthly_stats && !data.rows && !data.excludedkeys && !data.recent_reports && !data.fiscalyears && !data.report && !data.detail_rows && !data.export_forms && !data.themes_by_year && !data.fiscal_years) {
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
    // Server trusts client org only when BOTH are set; otherwise session pair is used.
    // Sending pref-only (common after login form) used to become 00/0021 and empty recent reports.
    if (!pref || !shokokai) {
      return {};
    }
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
