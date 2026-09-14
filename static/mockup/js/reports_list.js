(function () {
    var rows = Array.prototype.slice.call(document.querySelectorAll('#reports-tbody tr'));
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
    function isFederationRole() {
      var role = roleSelectEl ? roleSelectEl.value : 'shokokai';
      return role === 'national' || role === 'pref';
    }
    rows.forEach(function (tr) {
      var viewLink = tr.querySelector('.col-action a.btn');
      if (!viewLink) return;
      viewLink.addEventListener('click', function (e) {
        e.preventDefault();
        var cells = tr.children;
        var badgeElV = cells[0] ? cells[0].querySelector('.badge') : null;
        var formCodeV = badgeElV ? badgeElV.textContent.trim().split(/\s/)[0] : '';
        var formOptionV = document.querySelector('#mi-form option[value="' + CSS.escape(formCodeV) + '"]');
        var destScreenV = (formOptionV && formOptionV.dataset.screens) || (formCodeV === 'F' ? 'ai-input' : 'manual-input');
        var themeLabelV = cells[2] ? cells[2].textContent.trim() : '';
        var themeCheckboxV = Array.prototype.find.call(
          document.querySelectorAll('.mi-theme-checkbox'),
          (cb) => cb.dataset.label === themeLabelV
        );
        var staffTextV = cells[4] ? cells[4].textContent.trim() : '';
        var staffPartsV = staffTextV.split('／').map(s => s.trim());
        window.__miPendingPrefill = {
          content: cells[3] ? cells[3].textContent.trim() : '',
          themeCodes: themeCheckboxV ? [themeCheckboxV.value] : [],
          businessName: '',
          reportDate: cells[1] ? cells[1].textContent.trim() : '',
          staffMainName: staffPartsV[0] || '',
          staffSubName: staffPartsV[1] || '',
          formCode: formCodeV,
          timeStart: '',
          timeEnd: '',
          readOnly: isFederationRole(),
        };
        location.hash = '#' + destScreenV;
      });
    });
    if (typeof SelectWidth !== 'undefined') {
      SelectWidth.fit(elYearMonth);
      SelectWidth.fit(elPref);
      SelectWidth.fit(elShokokai);
      SelectWidth.fit(elForm);
      SelectWidth.fit(elTheme);

      SelectWidth.fitPlaceholder(elKeyword);
    }

    function matchesYearMonth(rowYearMonth, val) {

      if (val.indexOf('FY:') === 0) return true;
      return rowYearMonth === val;
    }
    function matchesForm(rowForm, val) {
      if (val === '全様式') return true;
      if (val === '様式F') return rowForm === 'F';
      if (val === '全様式G') return rowForm.indexOf('G-') === 0;
      return rowForm === val;
    }
    function applyFilter() {
      var yearMonthVal = elYearMonth.value;
      var formVal = elForm.value;
      var themeVal = elTheme.value;
      var includeDraft = elIncludeDraft.checked;
      var unprintedOnly = elUnprintedOnly.checked;
      var keyword = elKeyword.value.trim();
      var visible = 0;
      rows.forEach(function (tr) {
        var ok = matchesYearMonth(tr.dataset.yearmonth, yearMonthVal)
          && matchesForm(tr.dataset.form, formVal)
          && (themeVal === '' || tr.dataset.theme === themeVal)
          && (!includeDraft || tr.dataset.status === '下書き')
          && (!unprintedOnly || tr.dataset.printed === 'false')
          && (keyword === '' || tr.dataset.search.indexOf(keyword) !== -1);
        tr.style.display = ok ? '' : 'none';
        if (ok) visible++;
      });
      if (elCount) elCount.textContent = '全' + visible + '件';
      return visible;
    }

    function applyFilterWithFeedback() {
      var visible = applyFilter();
      Toast.success('絞り込みを更新しました（全' + visible + '件）');
    }
    [elYearMonth, elForm, elTheme, elIncludeDraft, elUnprintedOnly].forEach(function (el) {
      el.addEventListener('change', applyFilterWithFeedback);
    });
    elKeyword.addEventListener('input', applyFilter);
    applyFilter();

    window.__resetReportsFilters = function () {
      [elYearMonth, elPref, elShokokai, elForm, elTheme].forEach(function (sel) {
        Array.prototype.forEach.call(sel.options, function (opt) { opt.selected = opt.defaultSelected; });
      });
      elIncludeDraft.checked = elIncludeDraft.defaultChecked;
      elUnprintedOnly.checked = elUnprintedOnly.defaultChecked;
      elKeyword.value = elKeyword.defaultValue;
      if (typeof SelectWidth !== 'undefined') {
        SelectWidth.fit(elYearMonth);
        SelectWidth.fit(elPref);
        SelectWidth.fit(elShokokai);
        SelectWidth.fit(elForm);
        SelectWidth.fit(elTheme);
      }
      applyFilter();
    };

    var csvBtn = document.getElementById('reports-csv-btn');
    if (csvBtn) {
      csvBtn.addEventListener('click', function () {
        var header = ['様式', '実施日', '支援テーマ', '内容', '担当'];
        var visibleRows = rows.filter(function (tr) { return tr.style.display !== 'none'; });
        var lines = [header].concat(visibleRows.map(function (tr) {
          return Array.prototype.slice.call(tr.children).slice(0, 5).map(function (td) {
            return td.textContent.trim();
          });
        })).map(function (cols) {
          return cols.map(function (v) { return '"' + v.replace(/"/g, '""') + '"'; }).join(',');
        });
        var blob = new Blob(['\uFEFF' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = '報告書を見る_' + formatTimestamp(new Date()) + '.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        Toast.success('CSVを出力しました（表示中の' + visibleRows.length + '件）');
      });
    }
  })();
