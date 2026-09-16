// 事業所過去相談履歴（JigyoshomeiNoKohoKakoNoSodanRirekiHistoryAPI）
// 事業所名をキーにDB（trn_report＋mst_form＋mst_theme）から過去の相談履歴を実データで取得・表示する
function updateHistoryVisibility() {
  const jigyoshoEl = document.getElementById('mi-jigyosho');
  const emptyEl = document.getElementById('mi-history-empty');
  const stripEl = document.getElementById('mi-history-strip');
  if (!jigyoshoEl || !emptyEl || !stripEl) return;
  const hasBusiness = !!jigyoshoEl.value.trim();
  const noun = window.__miHistoryNoun || '相談';
  emptyEl.textContent = `事業所に紐づく${noun}履歴はありません。`;
  emptyEl.style.display = hasBusiness ? 'none' : '';
  stripEl.style.display = hasBusiness ? '' : 'none';
}

// 履歴行（実データ）を描画する
function renderHistory(rows) {
  const stripEl = document.getElementById('mi-history-strip');
  if (!stripEl) return;
  stripEl.innerHTML = '';
  rows.forEach((r) => {
    const item = document.createElement('div');
    item.className = 'mi-history-item';

    const top = document.createElement('div');
    top.className = 'mi-history-item__top';

    const date = document.createElement('span');
    date.className = 'mi-history-item__date';
    date.textContent = String(r.report_date || '').slice(0, 10);

    const theme = document.createElement('span');
    theme.className = 'mi-history-item__theme';
    theme.textContent = r.theme_label || '';

    const badge = document.createElement('span');
    badge.className = 'badge';
    badge.style.setProperty('--badge-color', r.form_badge_class || '#1a6fa8');
    badge.textContent = r.form_short_label || '';

    top.appendChild(date);
    top.appendChild(theme);
    top.appendChild(badge);

    const summary = document.createElement('div');
    summary.className = 'mi-history-item__summary';
    summary.textContent = r.summary || '';

    item.appendChild(top);
    item.appendChild(summary);
    stripEl.appendChild(item);
  });
}

let historySeq = 0;
let historyTimer = null;

// 過去相談履歴をAPI（実データ）から取得する
function loadHistory() {
  const jigyoshoEl = document.getElementById('mi-jigyosho');
  const stripEl = document.getElementById('mi-history-strip');
  if (!jigyoshoEl || !stripEl) return;
  const business = jigyoshoEl.value.trim();
  if (!business) {
    stripEl.innerHTML = '';
    return;
  }
  const my = ++historySeq;
  clearTimeout(historyTimer);
  historyTimer = setTimeout(() => {
    if (!window.ApiClient || typeof window.ApiClient.post !== 'function') return;
    // 組織情報（都道府県コード／商工会コード）を付与して履歴APIを呼び出す
    const body = Object.assign(
      { trnreportbusinessname: business, limit: '20' },
      (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {}
    );
    window.ApiClient.post('./jigyoshomeinokohokakonosodanrirekihistoryapi.do', body).then((result) => {
      if (my !== historySeq) return;
      const data = (result && result.data) || {};
      if (data.e) { renderHistory([]); return; }
      let raw = data.dragB;
      try { raw = typeof raw === 'string' ? JSON.parse(raw) : raw; } catch (e) { raw = []; }
      renderHistory(Array.isArray(raw) ? raw : []);
    }).catch(() => {
      if (my === historySeq) renderHistory([]);
    });
  }, 300);
}

// 帳票出力（FORMEXPORTAPI）反映後など他スクリプトから再取得できるよう公開する
window.__miLoadHistory = loadHistory;

(function () {
  const jigyoshoEl = document.getElementById('mi-jigyosho');

  if (jigyoshoEl) {
    jigyoshoEl.addEventListener('input', () => {
      updateHistoryVisibility();
      loadHistory();
    });
  }
  updateHistoryVisibility();
  // 帳票出力で事業所名が既に入っている場合は初期表示時に履歴を取得する
  loadHistory();
})();
