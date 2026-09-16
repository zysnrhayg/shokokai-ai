(function () {
  var tbody = document.getElementById('reports-tbody');
  if (!tbody) return;

  var elYearMonth = document.getElementById('f-yearmonth');
  var elPref = document.getElementById('reports-f-pref');
  var elShokokai = document.getElementById('reports-f-shokokai');
  var elForm = document.getElementById('f-form');
  var elTheme = document.getElementById('f-theme');
  var elIncludeDraft = document.getElementById('f-include-draft');
  var elUnprintedOnly = document.getElementById('f-unprinted-only');
  var elKeyword = document.getElementById('f-keyword');
  var elCount = document.getElementById('reports-count');
  var roleSelectEl = document.getElementById('org-role-select');

  var FISCAL_YEARS = [];
  var PREFECTURES = [];
  var SHOKOKAI_OPTIONS = [];
  var FORMS = [];
  var THEMES = [];
  var DEFAULT_YEAR_MONTH = '';
  var optionsReady = false;
  var loading = false;
  var pendingSearch = null;
  var keywordTimer = null;
  var allRows = [];
  var lastRows = [];

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function getCsrfToken() {
    if (window.ApiClient && typeof window.ApiClient.getCsrfToken === 'function') {
      return window.ApiClient.getCsrfToken();
    }
    var el = document.querySelector('input[name="csrf_token"]');
    return el ? el.value : '';
  }

  function currentUiRole() {
    return roleSelectEl ? roleSelectEl.value : 'shokokai';
  }

  function isFederationRole() {
    var role = currentUiRole();
    return role === 'national' || role === 'pref';
  }

  function orgFromClient() {
    if (window.ApiClient && typeof window.ApiClient.orgContext === 'function') {
      return window.ApiClient.orgContext() || {};
    }
    return {};
  }

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

  function parseDragB(data) {
    var raw = data && data.dragB;
    if (raw == null || raw === '') return [];
    if (Array.isArray(raw)) return raw;
    if (typeof raw === 'string') {
      try { return JSON.parse(raw); } catch (e) { return []; }
    }
    return [];
  }

  function postReportsApi(url, body) {
    if (window.ApiClient && typeof window.ApiClient.post === 'function') {
      return window.ApiClient.post(url, body);
    }
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
        try { data = text ? JSON.parse(text) : {}; } catch (e) { data = { e: text }; }
        return { ok: response.ok, status: response.status, data: data || {} };
      });
    });
  }

  function buildFilterPayload() {
    var role = currentUiRole();
    // national/pref: only use visible filter dropdowns (never localStorage org).
    // localStorage may keep login org '00' which has no reports.
    var pref = '';
    var sho = '';
    if (role === 'national') {
      pref = elPref && elPref.value ? elPref.value : '';
      sho = elShokokai && elShokokai.value ? elShokokai.value : '';
      if (pref === '00') pref = '';
    } else if (role === 'pref') {
      sho = elShokokai && elShokokai.value ? elShokokai.value : '';
    }
    var formVal = elForm ? elForm.value : '';
    if (formVal === '全様式') formVal = '';
    return {
      rolecode: role,
      prefecturecode: pref,
      shokokaicd: sho,
      yearmonth: elYearMonth ? elYearMonth.value : '',
      form: formVal,
      theme: elTheme ? elTheme.value : '',
      keyword: elKeyword ? elKeyword.value.trim() : '',
      includedraft: elIncludeDraft && elIncludeDraft.checked ? '1' : '',
      unprintedonly: elUnprintedOnly && elUnprintedOnly.checked ? '1' : '',
    };
  }

  function fitSelects() {
    if (typeof SelectWidth === 'undefined') return;
    SelectWidth.fit(elYearMonth);
    SelectWidth.fit(elPref);
    SelectWidth.fit(elShokokai);
    SelectWidth.fit(elForm);
    SelectWidth.fit(elTheme);
    SelectWidth.fitPlaceholder(elKeyword);
  }

  function fillYearMonth(keepValue) {
    if (!elYearMonth) return;
    var cur = keepValue ? elYearMonth.value : (DEFAULT_YEAR_MONTH || '');
    var html = '';
    FISCAL_YEARS.forEach(function (fy) {
      html += '<option value="FY:' + esc(fy.fiscal_year_code) + '">' + esc(fy.label) + '</option>';
      (fy.months || []).forEach(function (m) {
        html += '<option value="' + esc(m.value) + '">' + esc(m.label) + '</option>';
      });
    });
    elYearMonth.innerHTML = html || elYearMonth.innerHTML;
    if (cur && Array.prototype.some.call(elYearMonth.options, function (o) { return o.value === cur; })) {
      elYearMonth.value = cur;
    } else if (DEFAULT_YEAR_MONTH) {
      elYearMonth.value = DEFAULT_YEAR_MONTH;
    }
  }

  function fillPref(keepValue) {
    if (!elPref) return;
    var cur = keepValue ? elPref.value : '';
    elPref.innerHTML = '<option value="">全都道府県</option>' + PREFECTURES.map(function (p) {
      return '<option value="' + esc(p.prefecture_code) + '">' + esc(p.name) + '</option>';
    }).join('');
    if (cur && Array.prototype.some.call(elPref.options, function (o) { return o.value === cur; })) elPref.value = cur;
  }

  function fillShokokai(keepValue) {
    if (!elShokokai) return;
    var cur = keepValue ? elShokokai.value : '';
    var pref = elPref && elPref.value ? elPref.value : '';
    var list = SHOKOKAI_OPTIONS.filter(function (s) {
      return !pref || s.prefecture_code === pref;
    });
    elShokokai.innerHTML = '<option value="">全商工会</option>' + list.map(function (s) {
      return '<option value="' + esc(s.shokokai_cd) + '">' + esc(s.name) + '</option>';
    }).join('');
    if (cur && Array.prototype.some.call(elShokokai.options, function (o) { return o.value === cur; })) elShokokai.value = cur;
  }

  function fillForm(keepValue) {
    if (!elForm) return;
    var cur = keepValue ? elForm.value : '全様式';
    var html = '<option value="全様式">全様式（F・G）</option>';
    var hasF = FORMS.some(function (f) { return f.form_code === 'F'; });
    var hasG = FORMS.some(function (f) { return f.form_code && f.form_code.indexOf('G') === 0; });
    if (hasF) html += '<option value="様式F">F 相談受付票</option>';
    if (hasG) html += '<option value="全様式G">様式G（全種類）</option>';
    FORMS.forEach(function (f) {
      if (f.form_code === 'F') return;
      html += '<option value="' + esc(f.form_code) + '">' + esc(f.full_label || f.short_label || f.form_code) + '</option>';
    });
    elForm.innerHTML = html;
    if (cur && Array.prototype.some.call(elForm.options, function (o) { return o.value === cur; })) elForm.value = cur;
  }

  function fillTheme(keepValue) {
    if (!elTheme) return;
    var cur = keepValue ? elTheme.value : '';
    elTheme.innerHTML = '<option value="">全テーマ</option>' + THEMES.map(function (t) {
      return '<option value="' + esc(t.label) + '">' + esc(t.label) + '</option>';
    }).join('');
    if (cur && Array.prototype.some.call(elTheme.options, function (o) { return o.value === cur; })) elTheme.value = cur;
  }

  function applyInitOptions(data) {
    if (!data) return;
    if (Array.isArray(data.fiscalyears)) FISCAL_YEARS = data.fiscalyears;
    if (Array.isArray(data.prefectures)) PREFECTURES = data.prefectures;
    if (Array.isArray(data.shokokaioptions)) SHOKOKAI_OPTIONS = data.shokokaioptions;
    if (Array.isArray(data.forms)) FORMS = data.forms;
    if (Array.isArray(data.themes)) THEMES = data.themes;
    if (data.defaultyearmonth) DEFAULT_YEAR_MONTH = String(data.defaultyearmonth);
    fillYearMonth(false);
    fillPref(true);
    fillShokokai(true);
    fillForm(true);
    fillTheme(true);
    fitSelects();
    optionsReady = true;
  }

  function renderRows(rows) {
    lastRows = rows || [];
    if (!tbody) return;
    if (!lastRows.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-muted">該当する報告書はありません</td></tr>';
      if (elCount) elCount.textContent = '全0件';
      return;
    }
    tbody.innerHTML = lastRows.map(function (r) {
      var badge = r.form_badge_class || '#1a6fa8';
      var statusHtml = r.status === '下書き'
        ? '<span class="badge badge-status-pending">下書き</span> '
        : '';
      var content = statusHtml + esc(r.content || r.summary || '');
      return '<tr data-report-id="' + esc(r.report_id) + '"'
        + ' data-form="' + esc(r.form_code) + '"'
        + ' data-theme="' + esc(r.theme_label) + '"'
        + ' data-status="' + esc(r.status) + '">'
        + '<td><span class="badge" style="--badge-color:' + esc(badge) + '">' + esc(r.form_short_label || r.form_code) + '</span></td>'
        + '<td>' + esc(r.report_date) + '</td>'
        + '<td>' + esc(r.theme_label) + '</td>'
        + '<td>' + content + '</td>'
        + '<td>' + esc(r.staff_label) + '</td>'
        + '<td class="col-action"><a class="btn btn-primary btn-sm" href="#" data-report-view="' + esc(r.report_id) + '">閲覧</a></td>'
        + '</tr>';
    }).join('');
    if (elCount) elCount.textContent = '全' + lastRows.length + '件';
  }

  function handleResult(result, failMsg) {
    loading = false;
    var data = (result && result.data) || {};
    if (data.e) {
      toastError(String(data.e).trim());
      renderRows([]);
      return false;
    }
    if (!result.ok) {
      toastError(failMsg);
      renderRows([]);
      return false;
    }
    return true;
  }

  function yearMonthOf(row) {
    var d = String(row.report_date || '');
    return d.length >= 7 ? d.slice(0, 7) : '';
  }

  function fyRangeForCode(code) {
    for (var i = 0; i < FISCAL_YEARS.length; i++) {
      var fy = FISCAL_YEARS[i];
      if (fy.fiscal_year_code === code) {
        return { start: fy.start_month || '', end: fy.end_month || '' };
      }
    }
    return null;
  }

  // 顧客設計: 絞込・並び替えは get_visible_reports 結果に対してクライアント側で実施
  function filterRowsLocally() {
    var role = currentUiRole();
    var pref = elPref && elPref.value ? elPref.value : '';
    var sho = elShokokai && elShokokai.value ? elShokokai.value : '';
    if (pref === '00') pref = '';
    var yearVal = elYearMonth ? elYearMonth.value : '';
    var formVal = elForm ? elForm.value : '';
    if (formVal === '全様式') formVal = '';
    var themeVal = elTheme ? elTheme.value : '';
    var keyword = elKeyword ? elKeyword.value.trim().toLowerCase() : '';
    var draftOnly = elIncludeDraft && elIncludeDraft.checked;
    var unprintedOnly = elUnprintedOnly && elUnprintedOnly.checked;
    var fyStart = '';
    var fyEnd = '';
    var exactYm = '';
    if (yearVal && yearVal.indexOf('FY:') === 0) {
      var range = fyRangeForCode(yearVal.slice(3));
      if (range) { fyStart = range.start; fyEnd = range.end; }
    } else if (yearVal) {
      exactYm = yearVal;
    }
    return (allRows || []).filter(function (r) {
      if (role === 'national') {
        if (pref && r.prefecture_code !== pref) return false;
        if (sho && r.shokokai_cd !== sho) return false;
      } else if (role === 'pref') {
        if (sho && r.shokokai_cd !== sho) return false;
      }
      var ym = yearMonthOf(r);
      if (exactYm && ym !== exactYm) return false;
      if (!exactYm && fyStart && fyEnd && ym && (ym < fyStart || ym > fyEnd)) return false;
      var fc = r.form_code || '';
      if (formVal === '様式F' && fc !== 'F') return false;
      if (formVal === '全様式G' && (!fc || fc === 'F' || fc.indexOf('H') === 0 || fc.indexOf('I') === 0)) return false;
      if (formVal && formVal !== '様式F' && formVal !== '全様式G' && fc !== formVal) return false;
      if (themeVal && r.theme_label !== themeVal && r.theme_code !== themeVal) return false;
      if (keyword) {
        var blob = [
          r.summary, r.content, r.staff_main_name, r.staff_sub_name, r.staff_label, r.report_code
        ].join(' ').toLowerCase();
        if (blob.indexOf(keyword) < 0) return false;
      }
      if (draftOnly && r.status !== '下書き') return false;
      if (unprintedOnly && r.printed) return false;
      return true;
    });
  }

  function loadSearch(withToast) {
    var rows = filterRowsLocally();
    renderRows(rows);
    if (withToast) toastOk('絞り込みを更新しました（全' + rows.length + '件）');
  }

  function flushPendingSearch() {
    if (!pendingSearch) return;
    var next = pendingSearch;
    pendingSearch = null;
    loadSearch(next.withToast);
  }

  function loadInit() {
    if (loading) return;
    loading = true;
    tbody.innerHTML = '<tr><td colspan="6" class="text-muted">読み込み中...</td></tr>';
    var payload = buildFilterPayload();
    payload.yearmonth = '';
    payload.form = '';
    payload.theme = '';
    payload.keyword = '';
    payload.includedraft = '';
    payload.unprintedonly = '';
    postReportsApi('./reportsinitapi.do', payload)
      .then(function (result) {
        if (!handleResult(result, '報告書一覧の初期表示に失敗しました')) {
          flushPendingSearch();
          return;
        }
        applyInitOptions(result.data);
        allRows = parseDragB(result.data);
        loadSearch(false);
        flushPendingSearch();
      })
      .catch(function () {
        loading = false;
        toastError('報告書一覧の初期表示に失敗しました');
        allRows = [];
        renderRows([]);
        flushPendingSearch();
      });
  }

  function destScreenForForm(formCode) {
    var formOption = document.querySelector('#mi-form option[value="' + String(formCode || '').replace(/"/g, '\\"') + '"]');
    if (formOption && formOption.dataset.screens) return formOption.dataset.screens;
    return formCode === 'F' ? 'ai-input' : 'manual-input';
  }

  function openReport(reportId) {
    if (!reportId) return;
    postReportsApi('./reportdetailinitapi.do', { reportid: String(reportId) })
      .then(function (result) {
        var data = (result && result.data) || {};
        if (data.e) {
          toastError(String(data.e).trim());
          return;
        }
        if (!result.ok || !data.report) {
          toastError('報告書詳細の取得に失敗しました');
          return;
        }
        var d = data.report;
        window.__miPendingPrefill = {
          content: d.content || d.summary || '',
          themeCodes: Array.isArray(d.theme_codes) ? d.theme_codes : (d.primary_theme_code ? [d.primary_theme_code] : []),
          businessName: d.business_name || '',
          reportDate: d.report_date || '',
          staffMainName: d.staff_main_name || '',
          staffSubName: d.staff_sub_name || '',
          formCode: d.form_code || '',
          timeStart: d.time_start || '',
          timeEnd: d.time_end || '',
          readOnly: isFederationRole(),
        };
        location.hash = '#' + destScreenForForm(d.form_code);
      })
      .catch(function () {
        toastError('報告書詳細の取得に失敗しました');
      });
  }

  var CSV_VIEW_COLUMNS = [
    '様式', '都道府県連', '商工会', '報告書番号', '支援テーマ', '業種', '実施日',
    '開始時刻', '終了時刻', '事業所名', '担当者名', '概要', '内容',
    '音声入力の変換結果', '担当（主）', '担当（副）', '登録日'
  ];

  function downloadCsvFromRows(rows, columns) {
    var header = (columns && columns.length) ? columns : CSV_VIEW_COLUMNS;
    var lines = [header].concat((rows || []).map(function (r) {
      return header.map(function (col) { return r[col] != null ? r[col] : ''; });
    })).map(function (cols) {
      return cols.map(function (v) { return '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"'; }).join(',');
    });
    var blob = new Blob(['\uFEFF' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = '報告書を見る_' + (typeof formatTimestamp === 'function' ? formatTimestamp(new Date()) : Date.now()) + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toastOk('CSVを出力しました（' + (rows || []).length + '件）');
  }

  function exportCsv() {
    postReportsApi('./reportscsvexportapi.do', buildFilterPayload())
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
        downloadCsvFromRows(parseDragB(data), data.csvcolumns);
        // CSV出力後は printed_at 更新済み → ローカル一覧も印刷済みにして再絞込
        var exported = parseDragB(data) || [];
        var idSet = {};
        exported.forEach(function (r) { if (r.report_id != null) idSet[String(r.report_id)] = true; });
        allRows.forEach(function (r) {
          if (idSet[String(r.report_id)]) {
            r.printed = true;
            r.printed_at = r.printed_at || (new Date()).toISOString().slice(0, 10);
          }
        });
        loadSearch(false);
      })
      .catch(function () {
        toastError('CSV出力に失敗しました');
      });
  }

  tbody.addEventListener('click', function (e) {
    var link = e.target.closest('[data-report-view]');
    if (!link) return;
    e.preventDefault();
    openReport(link.getAttribute('data-report-view'));
  });

  [elYearMonth, elForm, elTheme, elIncludeDraft, elUnprintedOnly].forEach(function (el) {
    if (!el) return;
    el.addEventListener('change', function () { loadSearch(true); });
  });
  if (elPref) {
    elPref.addEventListener('change', function () {
      fillShokokai(false);
      fitSelects();
      loadSearch(true);
    });
  }
  if (elShokokai) {
    elShokokai.addEventListener('change', function () { loadSearch(true); });
  }
  if (elKeyword) {
    elKeyword.addEventListener('input', function () {
      if (keywordTimer) clearTimeout(keywordTimer);
      keywordTimer = setTimeout(function () { loadSearch(false); }, 400);
    });
  }

  var csvBtn = document.getElementById('reports-csv-btn');
  if (csvBtn) csvBtn.addEventListener('click', exportCsv);

  window.__resetReportsFilters = function () {
    if (elYearMonth) elYearMonth.value = DEFAULT_YEAR_MONTH || (elYearMonth.options[0] ? elYearMonth.options[0].value : '');
    if (elPref) elPref.value = '';
    fillShokokai(false);
    if (elForm) elForm.value = '全様式';
    if (elTheme) elTheme.value = '';
    if (elIncludeDraft) elIncludeDraft.checked = false;
    if (elUnprintedOnly) elUnprintedOnly.checked = false;
    if (elKeyword) elKeyword.value = '';
    fitSelects();
    loadSearch(false);
  };

  window.__renderReports = function () {
    loadInit();
  };
})();