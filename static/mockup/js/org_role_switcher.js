(function () {
  const roleSelect = document.getElementById('org-role-select');
  const orgNameEl = document.getElementById('org-name-display');
  if (!roleSelect || !orgNameEl) return;

  const ORG_NAME_BY_ROLE = {
    national: '全国商工会連合会',
    pref: '北海道商工会連合会',
    shokokai: '札幌商工会連合会',
  };

  function applyOrgRole(role) {
    orgNameEl.textContent = ORG_NAME_BY_ROLE[role] || ORG_NAME_BY_ROLE.pref;

    const COLOR_BY_ROLE = { national: 'var(--navy)', pref: 'var(--green)', shokokai: 'var(--purple)' };
    const isFederation = role === 'national' || role === 'pref';
    const sidebarHeaderEl = document.querySelector('.sidebar-header');
    if (sidebarHeaderEl) {
      sidebarHeaderEl.style.background = COLOR_BY_ROLE[role] || COLOR_BY_ROLE.pref;
    }

    const sidebarEl = document.querySelector('.sidebar');
    if (sidebarEl) {
      sidebarEl.style.background = COLOR_BY_ROLE[role] || COLOR_BY_ROLE.pref;
    }

    applyRoleAccentColor();
    const entrySection = document.getElementById('nav-section-entry');
    const knowledgeItem = document.getElementById('nav-item-knowledge');
    if (entrySection) entrySection.style.display = isFederation ? 'none' : '';
    if (knowledgeItem) knowledgeItem.style.display = isFederation ? '' : 'none';

    const reportsShokokaiField = document.getElementById('reports-f-shokokai-field');
    const accountsShokokaiField = document.getElementById('accounts-f-shokokai-field');
    if (reportsShokokaiField) reportsShokokaiField.style.display = isFederation ? '' : 'none';
    if (accountsShokokaiField) accountsShokokaiField.style.display = isFederation ? '' : 'none';

    const isNational = role === 'national';
    const reportsPrefField = document.getElementById('reports-f-pref-field');
    const accountsPrefField = document.getElementById('accounts-f-pref-field');
    if (reportsPrefField) reportsPrefField.style.display = isNational ? '' : 'none';
    if (accountsPrefField) accountsPrefField.style.display = isNational ? '' : 'none';
  }

  roleSelect.addEventListener('change', () => {
    applyOrgRole(roleSelect.value);
    if (typeof window.__renderHomeForRole === 'function') window.__renderHomeForRole(roleSelect.value);
    // 実績確認画面にいる場合はホームへ飛ばさずデータを再読込
    if ((location.hash || '').replace(/^#/, '') === 'monthly'
        && typeof window.__renderMonthly === 'function') {
      window.__renderMonthly();
      return;
    }
    location.hash = '#home';
  });
  applyOrgRole(roleSelect.value);
})();
