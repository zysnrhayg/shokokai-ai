(function () {
  const root = document.getElementById('knowledge-search-root');
  if (!root) return;

  const MAX_RESULTS = 4;
  let searchResults = null;
  let lastKeyword = '';
  let loading = false;
  let searchSeq = 0;

  function parseThemeBadges(raw) {
    if (!raw) return [];
    if (Array.isArray(raw)) return raw;
    if (typeof raw === 'string') {
      try {
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
      } catch (e) {
        return [];
      }
    }
    return [];
  }

  function firstSentence(text) {
    const body = String(text || '').trim();
    if (!body) return '';
    const idx = body.indexOf('。');
    return idx === -1 ? body : body.slice(0, idx + 1);
  }

  function formatDateTime(dt) {
    if (!dt) return '';
    const m = String(dt).match(/^(\d{4}-\d{2}-\d{2})(?:[ T](\d{2}:\d{2}))?/);
    if (m) return m[2] ? (m[1] + ' ' + m[2]) : m[1];
    return String(dt);
  }

  function mapRow(row) {
    const title = String(row.title || '').trim();
    const content = String(row.content || '').trim();
    const code = String(row.knowledge_code || '').trim();
    const badges = parseThemeBadges(row.theme_badges);
    return {
      code: code,
      title: title,
      content: content,
      theme_badges: badges,
      document_title: String(row.document_title || '').trim(),
      prefecture_name: String(row.prefecture_name || '').trim(),
      ref_info: firstSentence(content),
      updated_date: formatDateTime(row.updated_date)
    };
  }

  function toastError(msg) {
    try {
      if (typeof Toast !== 'undefined' && Toast.error) Toast.error(msg);
      else window.alert(msg);
    } catch (e) {
      window.alert(msg);
    }
  }

  function postSearch(keyword) {
    const body = Object.assign({
      mode: '1',
      actflg: '1',
      triggerid: 'knowledgesearchapi',
      keyword: keyword,
    }, (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {});
    if (window.ApiClient && typeof window.ApiClient.post === 'function') {
      return window.ApiClient.post('/knowledgesearchapi.do', body);
    }
    return Promise.reject(new Error('ApiClient unavailable'));
  }

  function alignResults() {
    if (typeof alignCardBottomToManualInput === 'function') {
      requestAnimationFrame(() => {
        alignCardBottomToManualInput(root.querySelector('#ks-results'), false);
      });
    }
  }

  function highlightText(text, keyword) {
    if (!keyword) return esc(text);
    const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(escapedKeyword, 'gi');
    let result = '';
    let lastIndex = 0;
    let m;
    while ((m = re.exec(text)) !== null) {
      result += esc(text.slice(lastIndex, m.index));
      result += `<mark>${esc(m[0])}</mark>`;
      lastIndex = m.index + m[0].length;
    }
    result += esc(text.slice(lastIndex));
    return result;
  }

  function formatKnowledgeBody(body, keyword) {
    const idx = body.indexOf('。');
    if (idx === -1) return highlightText(body, keyword);
    const lead = body.slice(0, idx + 1);
    const rest = body.slice(idx + 1);
    return `<strong>${highlightText(lead, keyword)}</strong>${rest ? `<br><br>${highlightText(rest, keyword)}` : ''}`;
  }

  function setBusy(isBusy) {
    loading = isBusy;
    const searchBtn = root.querySelector('#ks-search-btn');
    const clearBtn = root.querySelector('#ks-clear-btn');
    if (searchBtn) searchBtn.disabled = isBusy;
    if (clearBtn) clearBtn.disabled = isBusy;
  }

  function render() {
    root.innerHTML = `
      <div class="screen-body screen-body--fill">
        <div class="cat-lbl">🔍 検索条件を入力すると蓄積されたナレッジを検索できます</div>
        <div class="card" id="ks-search-card" style="margin-bottom:var(--space-6)">
          <div class="card-header card-header--navy"><div class="card-title card-title--white">🔍 検索条件</div></div>
          <div class="card-body" id="ks-search-header">
            <div class="flex items-end gap-md" style="width:100%;">
              <div class="filter-field" style="flex:1;">
                <div class="filter-field__label">検索したい内容</div>
                <input type="text" class="form-input" id="ks-keyword" placeholder="例：インボイス、賃上げ促進税制 など">
              </div>

              <div class="filter-field" style="align-self:stretch;">
                <div class="filter-field__label">&nbsp;</div>
                <button type="button" class="btn btn-primary--violet btn-sm" style="color:white; flex:1;" id="ks-search-btn">🔍 ナレッジを検索する</button>
              </div>
              <div class="filter-field" style="align-self:stretch;">
                <div class="filter-field__label">&nbsp;</div>
                <button type="button" class="btn btn-outline btn-sm" style="flex:1;" id="ks-clear-btn">✕ 検索内容をクリア</button>
              </div>
            </div>
          </div>
        </div>
        <div class="cat-lbl">
          <span>📚 検索結果<span id="ks-result-count" class="text-muted" style="font-weight:var(--fw-regular);margin-left:var(--space-3);"></span></span>
        </div>
        <div class="grid grid-gap-md" id="ks-results"></div>
      </div>
    `;
    const keywordEl = root.querySelector('#ks-keyword');
    keywordEl.value = lastKeyword;
    root.querySelector('#ks-search-btn').addEventListener('click', runSearch);
    keywordEl.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      if (e.isComposing || e.keyCode === 229) return;
      e.preventDefault();
      runSearch();
    });
    root.querySelector('#ks-clear-btn').addEventListener('click', () => {
      keywordEl.value = '';
      lastKeyword = '';
      keywordEl.focus();
      loadEntries('');
    });
    if (typeof window.__applyRoleAccentColor === 'function') window.__applyRoleAccentColor();
    loadEntries(lastKeyword || '');
  }

  function loadEntries(keyword) {
    const seq = ++searchSeq;
    lastKeyword = String(keyword || '');
    setBusy(true);
    renderResults();
    postSearch(lastKeyword).then(function (result) {
      if (seq !== searchSeq) return;
      setBusy(false);
      const data = (result && result.data) || {};
      if (!result || !result.ok || data.e) {
        searchResults = [];
        toastError(data.e || 'ナレッジ検索に失敗しました');
        renderResults();
        return;
      }
      const rows = Array.isArray(data.entries) ? data.entries : [];
      searchResults = rows.map(mapRow);
      renderResults();
    }).catch(function () {
      if (seq !== searchSeq) return;
      setBusy(false);
      searchResults = [];
      toastError('ナレッジ検索に失敗しました');
      renderResults();
    });
  }

  function runSearch() {
    const keywordEl = root.querySelector('#ks-keyword');
    const rawKeyword = keywordEl ? keywordEl.value.trim() : '';
    if (!rawKeyword) {
      toastError('キーワードを入力してください');
      keywordEl && keywordEl.focus();
      return;
    }
    loadEntries(rawKeyword);
  }

  function renderThemeBadges(entry) {
    const badges = entry.theme_badges || [];
    if (!badges.length) return '';
    return badges.map(function (t) {
      const color = t.badge_class || '#1a6fa8';
      return `<span class="badge" style="--badge-color:${esc(color)}">${highlightText(t.label || '', lastKeyword)}</span>`;
    }).join(' ');
  }

  function renderResults() {
    const resultsEl = root.querySelector('#ks-results');
    const countEl = root.querySelector('#ks-result-count');
    if (!resultsEl || !countEl) return;
    if (loading) {
      countEl.textContent = '';
      resultsEl.innerHTML = `<div class="text-muted text-sm" style="grid-column:1/-1">ナレッジを検索しています…</div>`;
      return;
    }
    if (!searchResults) {
      countEl.textContent = '';
      resultsEl.innerHTML = `<div class="text-muted text-sm" style="grid-column:1/-1">公開ナレッジを読み込んでいます…</div>`;
      alignResults();
      return;
    }
    if (!searchResults.length) {
      countEl.textContent = '';
      resultsEl.innerHTML = `<div class="text-muted text-sm" style="grid-column:1/-1">${lastKeyword ? '該当するナレッジが見つかりませんでした。別のキーワードをお試しください。' : '公開中のナレッジはありません。'}</div>`;
      alignResults();
      return;
    }

    const shown = searchResults.slice(0, MAX_RESULTS);
    countEl.textContent = searchResults.length > shown.length
      ? `（上位${shown.length}件を表示）`
      : `（${shown.length}件）`;
    resultsEl.innerHTML = shown.map(e => {
      const docPref = [
        e.document_title ? `文書：${esc(e.document_title)}` : '',
        e.prefecture_name ? `県：${esc(e.prefecture_name)}` : '',
      ].filter(Boolean).join(' ／ ');
      return `
      <div class="proposal-card proposal-card--mid">
        <div class="proposal-card__header">
          <div class="proposal-card__title">${highlightText(e.title, lastKeyword)}</div>
        </div>
        <div class="proposal-card__body">${formatKnowledgeBody(e.content, lastKeyword)}</div>
        <div class="proposal-card__meta">${renderThemeBadges(e)}</div>
        <div class="proposal-card__meta" style="margin-top:var(--space-2)"><strong>📚 参照したナレッジ：</strong>${esc(e.code)}${e.title ? '「' + esc(e.title) + '」' : ''}${e.ref_info ? '<br><strong>🔍 参照した情報：</strong>' + esc(e.ref_info) : ''}</div>
        ${docPref ? `<div class="proposal-card__meta">${docPref}</div>` : ''}
        <div class="proposal-card__meta"><strong>更新日時：</strong>${esc(e.updated_date)}</div>
      </div>
    `;
    }).join('');
    alignResults();
  }

  window.__renderKnowledgeSearch = () => {
    searchResults = null;
    lastKeyword = '';
    loading = false;
    searchSeq += 1;
    render();
  };
})();
