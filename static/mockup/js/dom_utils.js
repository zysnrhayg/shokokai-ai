function esc(value) {
  const div = document.createElement('div');
  div.textContent = value == null ? '' : String(value);
  return div.innerHTML;
}

function monthRange(startMonth, endMonth) {
  const months = [];
  let [y, m] = startMonth.split('-').map(Number);
  const [endY, endM] = endMonth.split('-').map(Number);
  while (y < endY || (y === endY && m <= endM)) {
    months.push(y + '-' + String(m).padStart(2, '0'));
    m++;
    if (m > 12) { m = 1; y++; }
  }
  return months;
}

function filterByPrefecture(options, prefectureCode) {
  return prefectureCode ? options.filter(s => s.prefecture_code === prefectureCode) : options;
}

document.querySelectorAll('.recent-reports-card tbody tr').forEach(bindRecentReportRow);

function bindRecentReportRow(tr) {
  const viewBtn = tr.querySelector('.col-action .btn');
  const badgeEl = tr.querySelector('td:first-child .badge');
  if (!viewBtn || !badgeEl || viewBtn.dataset.bound === '1') return;
  viewBtn.dataset.bound = '1';
  viewBtn.style.cursor = 'pointer';
  viewBtn.addEventListener('click', () => {

    const formCode = badgeEl.textContent.trim().split(/\s/)[0];
    const formOption = document.querySelector(`#mi-form option[value="${CSS.escape(formCode)}"]`);
    const destScreen = (formOption && formOption.dataset.screens) || (formCode === 'F' ? 'ai-input' : 'manual-input');
    const reportDate = tr.children[1] ? tr.children[1].textContent.trim() : '';
    const themeLabel = tr.children[2] ? tr.children[2].textContent.trim() : '';
    const content = tr.children[3] ? tr.children[3].textContent.trim() : '';
    const staffText = tr.children[4] ? tr.children[4].textContent.trim() : '';
    const [staffMainName, staffSubName] = staffText.split('／').map(s => s.trim());
    const themeCheckbox = Array.prototype.find.call(
      document.querySelectorAll('.mi-theme-checkbox'),
      (cb) => cb.dataset.label === themeLabel
    );
    window.__miPendingPrefill = {
      content,
      themeCodes: themeCheckbox ? [themeCheckbox.value] : [],
      businessName: tr.dataset.business || '',
      reportDate,
      staffMainName: staffMainName || '',
      staffSubName: staffSubName || '',
      formCode,
      timeStart: tr.dataset.timeStart || '',
      timeEnd: tr.dataset.timeEnd || '',
    };
    location.hash = '#' + destScreen;
  });
}

window.__bindRecentReportRows = function (scope) {
  (scope || document).querySelectorAll('.recent-reports-card tbody tr').forEach(bindRecentReportRow);
};

function syncSelectPlaceholder(select) {
  if (select) select.classList.toggle('is-placeholder', select.value === '');
}
function syncAllSelectPlaceholders(scope) {
  (scope || document).querySelectorAll('select.form-input').forEach(syncSelectPlaceholder);
}
document.addEventListener('change', (e) => {
  if (e.target instanceof HTMLSelectElement && e.target.matches('select.form-input')) syncSelectPlaceholder(e.target);
});
document.addEventListener('DOMContentLoaded', () => syncAllSelectPlaceholders());

function getHomeRecentReportsBottomOffset() {
  const homeView = document.getElementById('view-home');
  const card = homeView && homeView.querySelector('.recent-reports-card');
  const screenBody = homeView && homeView.querySelector('.screen-body');
  const mainMount = document.getElementById('main-mount');
  if (!homeView || !card || !screenBody || !mainMount) return null;
  const wasActive = homeView.classList.contains('active');
  if (!wasActive) {

    const width = mainMount.getBoundingClientRect().width;
    homeView.style.cssText = `display:block;position:fixed;visibility:hidden;top:0;left:0;width:${width}px;`;
  }
  const offset = card.getBoundingClientRect().bottom - screenBody.getBoundingClientRect().top;
  if (!wasActive) homeView.style.cssText = '';
  return offset > 0 ? offset : null;
}

function alignCardBottomToManualInput(cardEl, fixedHeight) {
  if (!cardEl) return;
  const screenBody = cardEl.closest('.screen-body');
  if (!screenBody) return;
  const refOffset = getHomeRecentReportsBottomOffset();
  if (!refOffset) return;
  const cardTopOffset = cardEl.getBoundingClientRect().top - screenBody.getBoundingClientRect().top;
  const targetHeight = refOffset - cardTopOffset;
  if (targetHeight <= 100) return;
  cardEl.style.minHeight = targetHeight + 'px';
  if (fixedHeight) cardEl.style.maxHeight = targetHeight + 'px';
}

function measureFilterHeaderHeight(viewId, headerSelector) {
  const view = document.getElementById(viewId);
  const header = view && view.querySelector(headerSelector);
  if (!view || !header) return null;
  const wasActive = view.classList.contains('active');
  const mainMount = document.getElementById('main-mount');
  if (!wasActive && mainMount) {
    const width = mainMount.getBoundingClientRect().width;
    view.style.cssText = `display:block;position:fixed;visibility:hidden;top:0;left:0;width:${width}px;`;
  }
  header.style.minHeight = '';
  const height = header.getBoundingClientRect().height;
  if (!wasActive) view.style.cssText = '';
  return height > 0 ? height : null;
}
function syncReportsMonthlyFilterHeaderHeight() {

  const targets = [
    ['view-reports', '#reports-filter-header'],
    ['view-monthly', '#monthly-filter-header'],
    ['view-accounts', '#accounts-filter-header'],
  ];
  const heights = targets.map(([viewId, sel]) => measureFilterHeaderHeight(viewId, sel));
  if (heights.some(h => !h)) return;
  const target = Math.max(...heights);
  const THRESHOLD_PX = 40;
  targets.forEach(([, sel], i) => {
    const el = document.querySelector(sel);
    if (!el) return;
    el.style.minHeight = (target - heights[i] <= THRESHOLD_PX) ? target + 'px' : '';
  });
}

function debounce(fn, delayMs) {
  let timerId = null;
  return (...args) => {
    if (timerId !== null) clearTimeout(timerId);
    timerId = setTimeout(() => fn(...args), delayMs);
  };
}

function logAiUsage(url, csrfToken, feature, input, output) {
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
    body: JSON.stringify({ feature, input, output }),
  }).catch(() => {});
}

function formatDate(d, sep) {
  const s = sep == null ? '-' : sep;
  return d.getFullYear() + s + String(d.getMonth() + 1).padStart(2, '0') + s + String(d.getDate()).padStart(2, '0');
}

function formatTimestamp(d) {
  const p = (n) => String(n).padStart(2, '0');
  return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate()) + p(d.getHours()) + p(d.getMinutes()) + p(d.getSeconds());
}

const FilterState = {
  save(key, ids) {
    const state = {};
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) state[id] = el.type === 'checkbox' ? el.checked : el.value;
    });
    sessionStorage.setItem('filter-state:' + key, JSON.stringify(state));
  },

  restore(key, ids) {
    const raw = sessionStorage.getItem('filter-state:' + key);
    if (!raw) return false;
    let state;
    try {
      state = JSON.parse(raw);
    } catch (e) {
      return false;
    }
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (!el || !Object.prototype.hasOwnProperty.call(state, id)) return;
      if (el.type === 'checkbox') el.checked = state[id];
      else el.value = state[id];
    });
    return true;
  },
};
