var ANNUAL_FORM_CODES = ['H', 'I-1', 'I-6', 'I-7', 'I-8'];

  function groupExportButtons() {
    var flatGroup = document.querySelector('#monthly-root .btn-group');
    if (!flatGroup || flatGroup.dataset.grouped) return;
    flatGroup.dataset.grouped = '1';

    var buttons = Array.prototype.slice.call(flatGroup.querySelectorAll('[data-export-form]'));
    var annualRow = document.createElement('div');
    annualRow.className = 'export-group';
    annualRow.innerHTML = '<span class="export-group__label">年に1回出力</span>';
    var monthlyRow = document.createElement('div');
    monthlyRow.className = 'export-group';
    monthlyRow.innerHTML = '<span class="export-group__label">毎月出力</span>';

    buttons.forEach(function (btn) {
      var code = btn.getAttribute('data-export-form');
      (ANNUAL_FORM_CODES.indexOf(code) !== -1 ? annualRow : monthlyRow).appendChild(btn);
    });

    var wrap = document.createElement('div');
    wrap.className = 'export-groups';
    if (annualRow.querySelector('[data-export-form]')) wrap.appendChild(annualRow);
    if (monthlyRow.querySelector('[data-export-form]')) wrap.appendChild(monthlyRow);

    flatGroup.replaceWith(wrap);
  }

  function insertCsvButton() {
    var header = document.querySelector('#monthly-table-card .card-header');
    if (!header || header.querySelector('#monthly-csv-btn')) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'monthly-csv-btn';
    btn.className = 'btn btn-outline btn-sm';
    btn.style.marginLeft = 'auto';
    btn.textContent = '⬇ CSV出力';
    btn.addEventListener('click', downloadCsv);
    header.appendChild(btn);
  }

  function downloadCsv() {
    var table = document.querySelector('#monthly-table-card table');
    if (!table) return;
    var lines = Array.prototype.slice.call(table.querySelectorAll('tr')).map(function (tr) {
      return Array.prototype.slice.call(tr.children).map(function (cell) {
        return '"' + cell.textContent.trim().replace(/"/g, '""') + '"';
      }).join(',');
    });

    var blob = new Blob(['\uFEFF' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob);
    var yearEl = document.getElementById('f-year');
    var a = document.createElement('a');
    a.href = url;
    a.download = '月次報告_' + (yearEl ? yearEl.value : '') + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    Toast.success('CSVを出力しました');
  }

  groupExportButtons();
  insertCsvButton();
  var yearSelect = document.getElementById('f-year');
  if (yearSelect) yearSelect.addEventListener('change', insertCsvButton);
