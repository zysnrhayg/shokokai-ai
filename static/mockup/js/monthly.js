(function () {
  const mockEl = document.getElementById('monthly-data');
  const MOCK_DATA = mockEl ? JSON.parse(mockEl.textContent) : null;
  let DATA = MOCK_DATA || {
    current_fiscal_year_code: '',
    fiscal_years: [],
    themes_by_year: {},
    detail_rows: [],
    total_rows: [],
    export_forms: [],
  };
  const root = document.getElementById('monthly-root');
  if (!root) return;

  let selectedYear = DATA.current_fiscal_year_code;
  let selectedMonth = null;
  let periodType = 'monthly'; // 'monthly' | 'annual'
  let loading = false;
  let initDone = false;
  let listReqSeq = 0; // 一覧再取得の競合防止

  const detailByKey = new Map();
  const totalByMonth = new Map();

  function rebuildMaps() {
    detailByKey.clear();
    totalByMonth.clear();
    (DATA.detail_rows || []).forEach(function (r) {
      detailByKey.set(String(r.theme_id) + '|' + r.year_month, Number(r.support_count) || 0);
    });
    (DATA.total_rows || []).forEach(function (r) {
      totalByMonth.set(r.year_month, Number(r.support_count) || 0);
    });
  }
  rebuildMaps();

  function toastError(msg) {
    try {
      if (typeof Toast !== 'undefined' && Toast.error) Toast.error(msg);
      else window.alert(msg);
    } catch (e) {
      window.alert(msg);
    }
  }

  function toastOk(msg) {
    try {
      if (typeof Toast !== 'undefined' && Toast.success) Toast.success(msg);
      else window.alert(msg);
    } catch (e) {
      window.alert(msg);
    }
  }

  function currentUiRole() {
    var el = document.getElementById('org-role-select');
    return el ? el.value : 'shokokai';
  }

  function postMonthlyApi(url, body) {
    if (window.ApiClient && typeof window.ApiClient.post === 'function') {
      return window.ApiClient.post(url, body);
    }
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': window.ApiClient && window.ApiClient.getCsrfToken
          ? window.ApiClient.getCsrfToken()
          : '',
      },
      body: JSON.stringify(body || {}),
    }).then(function (response) {
      return response.text().then(function (text) {
        var data = null;
        try { data = text ? JSON.parse(text) : {}; } catch (e) { data = { e: text }; }
        return { ok: response.ok, status: response.status, data: data || {} };
      });
    });
  }

  function buildPayload(extra) {
    var body = { rolecode: currentUiRole(), periodtype: periodType };
    if (window.ApiClient && typeof window.ApiClient.orgContext === 'function') {
      var org = window.ApiClient.orgContext() || {};
      if (org.prefecturecode) body.prefecturecode = org.prefecturecode;
      if (org.shokokaicd) body.shokokaicd = org.shokokaicd;
    }
    if (extra) {
      Object.keys(extra).forEach(function (k) {
        if (extra[k] != null && extra[k] !== '') body[k] = extra[k];
      });
    }
    return body;
  }

  function applyInitData(data, opts) {
    if (!data) return false;
    if (!Array.isArray(data.fiscal_years) || !data.fiscal_years.length) return false;
    opts = opts || {};
    DATA = {
      current_fiscal_year_code: data.current_fiscal_year_code || data.fiscal_years[0].fiscal_year_code,
      fiscal_years: data.fiscal_years,
      themes_by_year: data.themes_by_year || {},
      detail_rows: data.detail_rows || [],
      total_rows: data.total_rows || [],
      export_forms: data.export_forms || [],
    };
    if (!opts.keepSelection) {
      selectedYear = DATA.current_fiscal_year_code;
      selectedMonth = null;
    } else if (data.current_fiscal_year_code) {
      selectedYear = data.current_fiscal_year_code;
    }
    rebuildMaps();
    return true;
  }

  function reiwaLabel(yearMonth) {
    const [y, m] = yearMonth.split('-').map(Number);
    return '令和' + (y - 2018) + '年' + m + '月';
  }

  function render() {
    root.innerHTML = `
      <div class="screen-body screen-body--fill">
        <div class="cat-lbl">📄 帳票は指定した条件で出力、CSVは条件に関係なく一覧を出力します</div>

        <div class="card" id="monthly-filter-card">
          <div class="card-header" id="monthly-filter-header"${periodType === 'annual' ? ' class="is-annual"' : ''}>
            <div class="filter-row">
              <div class="filter-field" style="order:1;"><div class="filter-field__label">出力種別</div>
                <div class="flex items-center gap-md" style="height:36px; box-sizing:border-box;">
                  <label class="flex items-center gap-xs" style="white-space:nowrap;cursor:pointer;"><input type="radio" name="f-period-type" value="monthly"${periodType === 'monthly' ? ' checked' : ''}> 月次</label>
                  <label class="flex items-center gap-xs" style="white-space:nowrap;cursor:pointer;"><input type="radio" name="f-period-type" value="annual"${periodType === 'annual' ? ' checked' : ''}> 年次</label>
                </div>
              </div>
              <div class="filter-field" id="monthly-year-month-field"></div>
              <div class="filter-field" id="monthly-export-field">
                <div class="filter-field__label">帳票出力</div>
                <div class="flex items-center flex-wrap gap-xs" id="monthly-export-groups"></div>
              </div>
              <div class="filter-row__spacer" aria-hidden="true"></div>
              <div class="filter-field monthly-csv-field" style="border-left:1px solid var(--gold-border); padding-left:var(--space-6);">
                <div class="filter-field__label">&nbsp;</div>
                <div class="flex items-center gap-md">
                  <button type="button" class="btn btn-outline btn-sm" id="monthly-csv-btn" style="background:var(--surface-hover)">⬇ 一覧をCSVに出力する</button>
                </div>
              </div>
            </div>
          </div>
          <div id="monthly-table-card"></div>
        </div>
      </div>
    `;

    SelectWidth.fitAll(root);

    root.querySelectorAll('input[name="f-period-type"]').forEach(el => el.addEventListener('change', () => {
      var checked = root.querySelector('input[name="f-period-type"]:checked');
      var nextType = (checked && checked.value === 'annual') ? 'annual' : 'monthly';
      // 年次→月次：対象年度セレクトが消えるので最新年度へ戻す
      if (periodType === 'annual' && nextType === 'monthly') {
        var years = DATA.fiscal_years || [];
        if (years.length) {
          selectedYear = years[0].fiscal_year_code || selectedYear;
        }
        selectedMonth = null;
      }
      periodType = nextType;
      var headerEl = root.querySelector('#monthly-filter-header');
      if (headerEl) headerEl.classList.toggle('is-annual', periodType === 'annual');
      renderExportGroup();
      renderYearMonthField();
      // 月次↔年次：DB からテーマ一覧を取り直す（月次は実施年月で0件テーマ除外）
      refreshListFromDb();
    }));
    renderExportGroup();
    renderYearMonthField();

    root.querySelector('#monthly-csv-btn').addEventListener('click', downloadCsv);

    renderTable();
  }

  function filenameFromDisposition(header) {
    if (!header) return '';
    var m = /filename\*=UTF-8''([^;]+)|filename="?([^";]+)"?/i.exec(header);
    if (!m) return '';
    try {
      return decodeURIComponent((m[1] || m[2] || '').trim());
    } catch (e) {
      return (m[1] || m[2] || '').trim();
    }
  }

  function saveBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename || ('帳票_' + (typeof formatTimestamp === 'function' ? formatTimestamp(new Date()) : Date.now()));
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function isFileDownloadResponse(response) {
    var ct = (response.headers.get('content-type') || '').toLowerCase();
    var cd = (response.headers.get('content-disposition') || '').toLowerCase();
    if (cd.indexOf('attachment') >= 0) return true;
    if (ct.indexOf('application/json') >= 0) return false;
    if (ct.indexOf('text/json') >= 0) return false;
    if (ct.indexOf('text/html') >= 0) return false;
    if (ct.indexOf('text/plain') >= 0) return false;
    if (ct.indexOf('octet-stream') >= 0) return true;
    if (ct.indexOf('spreadsheet') >= 0 || ct.indexOf('excel') >= 0) return true;
    return false;
  }

  function exportFormMeta(formCode) {
    return (DATA.export_forms || []).find(function (f) {
      return f.form_code === formCode;
    });
  }

  function exportForm(formCode, formLabel) {
    var meta = exportFormMeta(formCode);
    var payload = buildPayload({
      formcode: formCode,
      fiscalyearcode: selectedYear || DATA.current_fiscal_year_code || '',
      yearmonth: (meta && meta.requires_yearmonth) ? (selectedMonth || '') : '',
    });
    var csrf = window.ApiClient && window.ApiClient.getCsrfToken
      ? window.ApiClient.getCsrfToken()
      : '';
    fetch('./monthlyexportapi.do', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
      },
      body: JSON.stringify(payload),
    })
      .then(function (response) {
        if (!isFileDownloadResponse(response)) {
          return response.text().then(function (text) {
            var data = {};
            try { data = text ? JSON.parse(text) : {}; } catch (e) { data = { e: text }; }
            toastError((data && data.e) ? String(data.e).trim() : '帳票出力に失敗しました');
          });
        }
        if (!response.ok) {
          toastError('帳票出力に失敗しました');
          return null;
        }
        return response.blob().then(function (blob) {
          var name = filenameFromDisposition(response.headers.get('content-disposition'))
            || ((formLabel || formCode) + '.xlsx');
          saveBlob(blob, name);
          toastOk((formLabel || formCode) + 'を出力しました');
        });
      })
      .catch(function () {
        toastError('帳票出力に失敗しました');
      });
  }

  function refreshListFromDb() {
    var extra = {
      fiscalyearcode: selectedYear || DATA.current_fiscal_year_code || '',
    };
    // 月次のみ yearmonth を渡し、当該月 support_count=0 のテーマをサーバ側で除外
    if (periodType === 'monthly' && selectedMonth) {
      extra.yearmonth = selectedMonth;
    }
    var seq = ++listReqSeq;
    postMonthlyApi('./monthlyinitapi.do', buildPayload(extra))
      .then(function (result) {
        if (seq !== listReqSeq) return; // 古い応答は捨てる
        var data = (result && result.data) || {};
        if (data.e) {
          toastError(String(data.e).trim());
          renderTable();
          return;
        }
        if (!result.ok || !applyInitData(data, { keepSelection: true })) {
          renderTable();
          return;
        }
        renderExportGroup();
        renderTable();
      })
      .catch(function () {
        if (seq !== listReqSeq) return;
        toastError('一覧の更新に失敗しました');
        renderTable();
      });
  }

  function switchFiscalYear(yearCode) {
    if (!yearCode || yearCode === selectedYear) {
      selectedYear = yearCode;
      renderTable();
      return;
    }
    var prevYear = selectedYear;
    var extra = { fiscalyearcode: yearCode };
    if (periodType === 'monthly' && selectedMonth) {
      extra.yearmonth = selectedMonth;
    }
    postMonthlyApi('./monthlyfiscalyearapi.do', buildPayload(extra))
      .then(function (result) {
        var data = (result && result.data) || {};
        if (data.e) {
          toastError(String(data.e).trim());
          selectedYear = prevYear;
          renderYearMonthField();
          renderTable();
          return;
        }
        if (!result.ok || !applyInitData(data, { keepSelection: true })) {
          selectedYear = prevYear;
          renderYearMonthField();
          renderTable();
          return;
        }
        selectedYear = DATA.current_fiscal_year_code || yearCode;
        render();
        // 年次：対象年度切替後も DB 一覧を再取得（年度合計0のテーマ除外）
        // 月次：実施年月条件で再取得
        refreshListFromDb();
      })
      .catch(function () {
        toastError('年度切替に失敗しました');
        selectedYear = prevYear;
        renderYearMonthField();
        renderTable();
      });
  }

  function renderExportGroup() {
    const groupsEl = root.querySelector('#monthly-export-groups');
    if (!groupsEl) return;
    const formsSrc = DATA.export_forms || [];
    if (!formsSrc.length) {
      groupsEl.innerHTML = '<span class="text-muted text-sm">出力できる帳票がありません</span>';
      return;
    }
    const checked = root.querySelector('input[name="f-period-type"]:checked');
    const isAnnual = checked && checked.value === 'annual';
    const wantGroup = isAnnual ? 'annual' : 'monthly';
    const forms = formsSrc.filter(function (f) {
      return (f.period_group || 'monthly') === wantGroup;
    });
    groupsEl.innerHTML = forms.length
      ? forms.map(f => `<button type="button" class="btn btn-outline btn-sm" data-export-form="${esc(f.form_code)}" data-export-label="${esc(f.full_label)}">${esc(f.short_label)}</button>`).join('')
      : `<span class="text-muted text-sm">出力できる帳票がありません</span>`;
    groupsEl.querySelectorAll('[data-export-form]').forEach(btn => {
      btn.addEventListener('click', () => {
        exportForm(btn.getAttribute('data-export-form'), btn.getAttribute('data-export-label'));
      });
    });
  }

  function renderYearMonthField() {
    const fieldEl = root.querySelector('#monthly-year-month-field');
    if (!fieldEl) return;
    const checked = root.querySelector('input[name="f-period-type"]:checked');
    const isAnnual = checked && checked.value === 'annual';
    const years = DATA.fiscal_years || [];

    if (isAnnual) {
      fieldEl.innerHTML = `
        <div class="filter-field__label">対象年度</div>
        <select class="form-input form-input--compact" style="width:110px;height:36px;box-sizing:border-box;" id="f-year">
          ${years.slice().reverse().map(fy => `<option value="${fy.fiscal_year_code}" ${fy.fiscal_year_code === selectedYear ? 'selected' : ''}>${fy.label}</option>`).join('')}
        </select>
      `;
      const yearEl = fieldEl.querySelector('#f-year');
      if (yearEl) {
        yearEl.addEventListener('change', (e) => {
          switchFiscalYear(e.target.value);
        });
      }
    } else {
      const fy = years.find(f => f.fiscal_year_code === selectedYear) || years[0];
      const months = fy ? monthRange(fy.start_month, fy.end_month) : [];

      if (!selectedMonth || !months.includes(selectedMonth)) {
        const now = new Date();
        const todayYm = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
        selectedMonth = months.includes(todayYm) ? todayYm : months[months.length - 1];
      }
      fieldEl.innerHTML = `
        <div class="filter-field__label">実施年月</div>
        <select class="form-input form-input--compact" style="width:110px;height:36px;box-sizing:border-box;" id="f-month">
          ${months.slice().reverse().map(ym => `<option value="${ym}" ${ym === selectedMonth ? 'selected' : ''}>${reiwaLabel(ym)}</option>`).join('')}
        </select>
      `;
      const monthEl = fieldEl.querySelector('#f-month');
      if (monthEl) {
        monthEl.addEventListener('change', (e) => {
          selectedMonth = e.target.value;
          refreshListFromDb();
        });
      }
    }
    SelectWidth.fitAll(fieldEl);
  }

  function renderTable() {
    const card = root.querySelector('#monthly-table-card');
    if (!card) return;
    if (loading && !initDone) {
      card.innerHTML = '<div class="text-muted" style="padding:var(--space-4);">読み込み中...</div>';
      return;
    }
    const fy = (DATA.fiscal_years || []).find(f => f.fiscal_year_code === selectedYear) || (DATA.fiscal_years || [])[0];
    const months = fy ? monthRange(fy.start_month, fy.end_month) : [];
    const themes = (DATA.themes_by_year && DATA.themes_by_year[selectedYear]) || [];

    const monthlyForTheme = (themeId) => {
      const monthly = {};
      months.forEach(ym => { monthly[ym] = detailByKey.get(String(themeId) + '|' + ym) || 0; });
      return monthly;
    };
    // 合計は total_rows（組織KPI）をそのまま表示（原設計: API129 相当）
    const totalMonthly = {};
    months.forEach(ym => { totalMonthly[ym] = totalByMonth.get(ym) || 0; });

    const monthCell = (monthly, ym, strong) => {
      const val = (monthly[ym] || 0).toLocaleString();
      return `<td class="num">${strong ? `<strong>${val}</strong>` : val}</td>`;
    };
    const rowTotal = (monthly) => months.reduce((sum, ym) => sum + (monthly[ym] || 0), 0);

    card.innerHTML = `
        <div class="table-scroll">
          <table>
            <thead>
              <tr>
                <th>支援テーマ</th>
                ${months.map(ym => `<th class="num">${reiwaLabel(ym)}</th>`).join('')}
                <th class="num">累計</th>
              </tr>
            </thead>
            <tbody>
              ${themes.length ? themes.map(theme => {
                const monthly = monthlyForTheme(theme.theme_id);
                return `
                <tr>
                  <td>${esc(theme.label)}</td>
                  ${months.map(ym => monthCell(monthly, ym, false)).join('')}
                  <td class="num">${rowTotal(monthly).toLocaleString()}</td>
                </tr>`;
              }).join('') : `<tr><td colspan="${months.length + 2}" class="text-muted">表示するテーマがありません</td></tr>`}
            </tbody>
            <tfoot>
              <tr class="total">
                <td><strong>合計</strong></td>
                ${months.map(ym => monthCell(totalMonthly, ym, true)).join('')}
                <td class="num"><strong>${rowTotal(totalMonthly).toLocaleString()}</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>
    `;
  }

  function parseDragB(data) {
    var raw = data && data.dragB;
    if (raw == null || raw === '') return [];
    if (Array.isArray(raw)) return raw;
    if (typeof raw === 'string') {
      try { return JSON.parse(raw); } catch (e) { return []; }
    }
    return [];
  }

  function downloadCsvFromRows(rows, filename) {
    rows = rows || [];
    if (!rows.length) {
      toastError('出力対象のデータがありません');
      return;
    }
    var lines = rows.map(function (cols) {
      return (cols || []).map(function (v) {
        return '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"';
      }).join(',');
    });
    var blob = new Blob([String.fromCharCode(0xFEFF) + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename || ('報告実績の確認・月次／年次帳票を出力する_' + (typeof formatTimestamp === 'function' ? formatTimestamp(new Date()) : Date.now()) + '.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function downloadCsv() {
    // 条件に関係なく一覧を出力（実施年月など画面絞り込みは送らない）
    var extra = {
      fiscalyearcode: selectedYear || DATA.current_fiscal_year_code || '',
    };
    postMonthlyApi('./monthlycsvexportapi.do', buildPayload(extra))
      .then(function (result) {
        var data = (result && result.data) || {};
        if (data.e) {
          toastError(String(data.e).trim());
          return;
        }
        if (!result.ok) {
          toastError('CSV出力に失敗しました');
          return;
        }
        var rows = parseDragB(data);
        if (!rows.length) {
          toastError('出力対象のデータがありません');
          return;
        }
        var name = data.filename || '報告実績の確認・月次／年次帳票を出力する.csv';
        if (typeof formatTimestamp === 'function' && name.indexOf('.csv') > 0) {
          name = name.replace(/\.csv$/i, '_' + formatTimestamp(new Date()) + '.csv');
        }
        downloadCsvFromRows(rows, name);
        toastOk('CSVを出力しました');
      })
      .catch(function () {
        toastError('CSV出力に失敗しました');
      });
  }

  function loadInit() {
    if (loading) return;
    loading = true;
    render();
    postMonthlyApi('./monthlyinitapi.do', buildPayload())
      .then(function (result) {
        loading = false;
        initDone = true;
        var data = (result && result.data) || {};
        if (data.e) {
          toastError(String(data.e).trim());
          render();
          return;
        }
        if (!result.ok || !applyInitData(data)) {
          if (!MOCK_DATA) toastError('実績確認・帳票出力の初期表示に失敗しました');
          render();
          return;
        }
        render();
        // 月次初期：実施年月確定後に DB で0件テーマを除外
        if (periodType === 'monthly' && selectedMonth) {
          refreshListFromDb();
        }
      })
      .catch(function () {
        loading = false;
        initDone = true;
        if (!MOCK_DATA) toastError('実績確認・帳票出力の初期表示に失敗しました');
        render();
      });
  }

  window.__renderMonthly = function () {
    loadInit();
  };

  loadInit();

  if (location.hash) {
    const target = document.querySelector(location.hash);
    if (target) target.scrollIntoView();
  }
})();
