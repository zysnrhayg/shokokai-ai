(function () {
  const DATA = JSON.parse(document.getElementById('monthly-data').textContent);
  const root = document.getElementById('monthly-root');
  if (!root) return;

  let selectedYear = DATA.current_fiscal_year_code;
  let selectedMonth = null;

  const ANNUAL_FORM_CODES = ['H', 'I-1', 'I-7', 'I-8'];

  const detailByKey = new Map();
  DATA.detail_rows.forEach(r => detailByKey.set(r.theme_id + '|' + r.year_month, r.support_count));
  const totalByMonth = new Map();
  DATA.total_rows.forEach(r => totalByMonth.set(r.year_month, r.support_count));

  function reiwaLabel(yearMonth) {
    const [y, m] = yearMonth.split('-').map(Number);
    return '令和' + (y - 2018) + '年' + m + '月';
  }

  function render() {
    root.innerHTML = `
      <div class="screen-body screen-body--fill">
        <div class="cat-lbl">📄 帳票は指定した条件で出力、CSVは条件に関係なく一覧を出力します</div>

        <div class="card" id="monthly-filter-card">
          <div class="card-header" id="monthly-filter-header">
            <div class="filter-row">
              <div class="filter-field"><div class="filter-field__label">出力種別</div>
                <div class="flex items-center gap-md" style="height:36px; box-sizing:border-box;">
                  <label class="flex items-center gap-xs" style="white-space:nowrap;cursor:pointer;"><input type="radio" name="f-period-type" value="monthly" checked> 月次</label>
                  <label class="flex items-center gap-xs" style="white-space:nowrap;cursor:pointer;"><input type="radio" name="f-period-type" value="annual"> 年次</label>
                </div>
              </div>
              <div class="filter-field" id="monthly-year-month-field"></div>
              <div class="filter-field" style="margin-left:auto;">
                <div class="filter-field__label">帳票出力</div>
                <div class="flex items-center gap-xs" id="monthly-export-groups"></div>
              </div>
              <div class="filter-field" style="border-left:1px solid var(--gold-border); padding-left:var(--space-6);">
                <div class="filter-field__label">&nbsp;</div>
                <div class="flex items-center gap-md">
                  <button type="button" class="btn btn-outline btn-sm" id="monthly-csv-btn">⬇ 一覧をCSVに出力する</button>
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
      renderExportGroup();
      renderYearMonthField();
    }));
    renderExportGroup();
    renderYearMonthField();

    root.querySelector('#monthly-csv-btn').addEventListener('click', downloadCsv);

    renderTable();
  }

  function renderExportGroup() {
    const groupsEl = root.querySelector('#monthly-export-groups');
    if (!groupsEl || !DATA.export_forms.length) return;
    const checked = root.querySelector('input[name="f-period-type"]:checked');
    const isAnnual = checked && checked.value === 'annual';
    const forms = DATA.export_forms.filter(f => ANNUAL_FORM_CODES.includes(f.form_code) === isAnnual);
    groupsEl.innerHTML = forms.length
      ? forms.map(f => `<button type="button" class="btn btn-outline btn-sm" data-export-form="${esc(f.form_code)}" data-export-label="${esc(f.full_label)}">${esc(f.short_label)}</button>`).join('')
      : `<span class="text-muted text-sm">出力できる帳票がありません</span>`;
    groupsEl.querySelectorAll('[data-export-form]').forEach(btn => {
      btn.addEventListener('click', () => {
        Toast.success(`${btn.getAttribute('data-export-label')}を出力しました`);
      });
    });
  }

  function renderYearMonthField() {
    const fieldEl = root.querySelector('#monthly-year-month-field');
    if (!fieldEl) return;
    const checked = root.querySelector('input[name="f-period-type"]:checked');
    const isAnnual = checked && checked.value === 'annual';

    if (isAnnual) {
      fieldEl.innerHTML = `
        <div class="filter-field__label">対象年度</div>
        <select class="form-input form-input--compact" style="width:110px;height:36px;box-sizing:border-box;" id="f-year">
          ${DATA.fiscal_years.slice().reverse().map(fy => `<option value="${fy.fiscal_year_code}" ${fy.fiscal_year_code === selectedYear ? 'selected' : ''}>${fy.label}</option>`).join('')}
        </select>
      `;
      fieldEl.querySelector('#f-year').addEventListener('change', (e) => {
        selectedYear = e.target.value;
        renderTable();
      });
    } else {
      const fy = DATA.fiscal_years.find(f => f.fiscal_year_code === selectedYear) || DATA.fiscal_years[0];
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
      fieldEl.querySelector('#f-month').addEventListener('change', (e) => {
        selectedMonth = e.target.value;
      });
    }
    SelectWidth.fitAll(fieldEl);
  }

  function renderTable() {
    const fy = DATA.fiscal_years.find(f => f.fiscal_year_code === selectedYear) || DATA.fiscal_years[0];
    const months = fy ? monthRange(fy.start_month, fy.end_month) : [];
    const themes = DATA.themes_by_year[selectedYear] || [];

    const monthlyForTheme = (themeId) => {
      const monthly = {};
      months.forEach(ym => { monthly[ym] = detailByKey.get(themeId + '|' + ym) || 0; });
      return monthly;
    };
    const totalMonthly = {};
    months.forEach(ym => { totalMonthly[ym] = totalByMonth.get(ym) || 0; });

    const monthCell = (monthly, ym, strong) => {
      const val = (monthly[ym] || 0).toLocaleString();
      return `<td class="num">${strong ? `<strong>${val}</strong>` : val}</td>`;
    };
    const rowTotal = (monthly) => months.reduce((sum, ym) => sum + (monthly[ym] || 0), 0);

    root.querySelector('#monthly-table-card').innerHTML = `
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
              ${themes.map(theme => {
                const monthly = monthlyForTheme(theme.theme_id);
                return `
                <tr>
                  <td>${esc(theme.label)}</td>
                  ${months.map(ym => monthCell(monthly, ym, false)).join('')}
                  <td class="num">${rowTotal(monthly).toLocaleString()}</td>
                </tr>`;
              }).join('')}
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

  function downloadCsv() {
    const table = root.querySelector('#monthly-table-card table');
    if (!table) return;
    const lines = Array.from(table.querySelectorAll('tr')).map(tr =>
      Array.from(tr.children).map(cell => '"' + cell.textContent.trim().replace(/"/g, '""') + '"').join(',')
    );

    const blob = new Blob([String.fromCharCode(0xFEFF) + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `報告実績の確認・月次／年次帳票を出力する_${formatTimestamp(new Date())}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    Toast.success('CSVを出力しました');
  }

  window.__renderMonthly = () => {
    selectedYear = DATA.current_fiscal_year_code;
    render();
  };
  render();

  if (location.hash) {
    const target = document.querySelector(location.hash);
    if (target) target.scrollIntoView();
  }
})();
