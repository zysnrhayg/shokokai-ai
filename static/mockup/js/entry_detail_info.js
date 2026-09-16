// 事業所に紐づく詳細情報（JigyoshomeiNoKohoKakoNoSodanRirekiNamesAPI）
// 組織に紐づく過去登録済みの事業所名一覧を取得し、Grid（20行改ページ）で表示する
(function () {
  var dropdownEl = document.getElementById('mi-detail-info-dropdown');
  var tbodyEl = document.getElementById('mi-detail-info-tbody');
  var pageInfoEl = document.getElementById('mi-detail-info-page-info');
  var prevBtn = document.getElementById('mi-detail-info-prev');
  var nextBtn = document.getElementById('mi-detail-info-next');
  if (!dropdownEl || !tbodyEl) return;

  var PAGE_SIZE = 20;
  var allRows = [];
  var currentPage = 1;
  var loaded = false;

  // Gridのページを描画する
  function renderPage() {
    var totalPages = Math.max(1, Math.ceil(allRows.length / PAGE_SIZE));
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    var start = (currentPage - 1) * PAGE_SIZE;
    var end = start + PAGE_SIZE;
    var pageRows = allRows.slice(start, end);

    tbodyEl.innerHTML = '';
    if (!pageRows.length) {
      var tr = document.createElement('tr');
      var td = document.createElement('td');
      td.colSpan = 2;
      td.style.padding = '6px 8px';
      td.style.color = 'var(--c-text-sub,#888)';
      td.textContent = '事業所名がありません';
      tr.appendChild(td);
      tbodyEl.appendChild(tr);
    } else {
      pageRows.forEach(function (r) {
        var tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.addEventListener('click', function () {
          // 事業所名を入力欄に反映し、過去履歴を再取得する
          var input = document.getElementById('mi-jigyosho');
          if (input) {
            input.value = r.business_name || '';
            input.dispatchEvent(new Event('input'));
          }
        });

        var tdName = document.createElement('td');
        tdName.style.padding = '6px 8px';
        tdName.style.borderBottom = '1px solid var(--c-border,#eee)';
        tdName.textContent = r.business_name || '';

        var tdDate = document.createElement('td');
        tdDate.style.padding = '6px 8px';
        tdDate.style.borderBottom = '1px solid var(--c-border,#eee)';
        tdDate.textContent = String(r.last_report_date || '').slice(0, 10);

        tr.appendChild(tdName);
        tr.appendChild(tdDate);
        tbodyEl.appendChild(tr);
      });
    }

    if (pageInfoEl) {
      pageInfoEl.textContent = currentPage + ' / ' + totalPages + ' ページ（全' + allRows.length + '件）';
    }
    if (prevBtn) prevBtn.disabled = currentPage <= 1;
    if (nextBtn) nextBtn.disabled = currentPage >= totalPages;
  }

  // APIから事業所名一覧を取得する
  function loadData() {
    if (loaded) { renderPage(); return; }
    if (!window.ApiClient || typeof window.ApiClient.post !== 'function') return;
    // 組織情報（都道府県コード／商工会コード）を付与してAPIを呼び出す
    var body = Object.assign(
      { limit: '20' },
      (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {}
    );
    tbodyEl.innerHTML = '<tr><td colspan="2" style="padding:6px 8px;color:var(--c-text-sub,#888);">読み込み中...</td></tr>';

    window.ApiClient.post('./jigyoshomeinokohokakonosodanrirekinamesapi.do', body).then(function (result) {
      var data = (result && result.data) || {};
      var raw = data.dragB;
      try { raw = typeof raw === 'string' ? JSON.parse(raw) : raw; } catch (e) { raw = []; }
      allRows = Array.isArray(raw) ? raw : [];
      loaded = true;
      currentPage = 1;
      renderPage();
    }).catch(function () {
      allRows = [];
      loaded = true;
      renderPage();
    });
  }

  // パネル展開時にデータを取得する
  dropdownEl.addEventListener('toggle', function () {
    if (dropdownEl.open) loadData();
  });

  // 改ページボタン
  if (prevBtn) prevBtn.addEventListener('click', function (e) {
    e.preventDefault();
    currentPage--;
    renderPage();
  });
  if (nextBtn) nextBtn.addEventListener('click', function (e) {
    e.preventDefault();
    currentPage++;
    renderPage();
  });
})();
