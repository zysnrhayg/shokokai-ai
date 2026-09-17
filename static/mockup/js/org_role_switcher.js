(function () {
  const roleSelect = document.getElementById('org-role-select');
  const orgNameEl = document.getElementById('org-name-display');
  if (!roleSelect || !orgNameEl) return;

  function applySessionProfile(profile) {
    profile = profile || {};
    var userid = profile.userid
      || (typeof localStorage !== 'undefined' && localStorage.getItem('userid'))
      || '';
    var username = profile.username
      || (typeof localStorage !== 'undefined' && localStorage.getItem('username'))
      || '';
    var orgname = profile.orgname
      || (typeof localStorage !== 'undefined' && localStorage.getItem('orgname'))
      || '';
    if (orgname) {
      orgNameEl.textContent = orgname;
      if (typeof localStorage !== 'undefined') localStorage.setItem('orgname', orgname);
    }
    var userInfo = document.querySelector('.user-info');
    if (userInfo && (userid || username)) {
      userInfo.textContent = userid + (username ? '：' + username : '');
    }
    if (userid && typeof localStorage !== 'undefined') localStorage.setItem('userid', userid);
    if (username && typeof localStorage !== 'undefined') localStorage.setItem('username', username);
  }
  window.__applySessionProfile = applySessionProfile;

  function showNav(route, on) {
    var el = document.querySelector('.sidebar .nav-item[data-route="' + route + '"]');
    if (el) el.style.display = on ? '' : 'none';
  }

  function applyMenuVisibility(menus) {
    var routes = {};
    (menus || []).forEach(function (m) {
      if (m && m.route) routes[m.route] = true;
    });
    if (!Object.keys(routes).length) return;

    showNav('home', !!routes.home);
    showNav('ai-input', !!routes['ai-input']);
    showNav('manual-input', !!routes['manual-input']);
    showNav('expert-import', !!routes['expert-import']);
    showNav('reports', !!routes.reports);
    showNav('monthly', !!routes.monthly);
    showNav('ai-proposal', !!routes['ai-proposal']);
    showNav('knowledge-search', !!routes['knowledge-search']);
    showNav('accounts', !!routes.accounts);
    showNav('knowledge', !!routes.knowledge);

    var entrySection = document.getElementById('nav-section-entry');
    if (entrySection) {
      var anyEntry = routes['ai-input'] || routes['manual-input'] || routes['expert-import'];
      entrySection.style.display = anyEntry ? '' : 'none';
    }
    var knowledgeItem = document.getElementById('nav-item-knowledge');
    if (knowledgeItem) knowledgeItem.style.display = routes.knowledge ? '' : 'none';
  }
  window.__applyMenuVisibility = applyMenuVisibility;

  /** Init 前のロール切替ですぐに項目単位の表示を合わせる（前回 menus の残留を消す） */
  function applyRoleMenuFallback(role) {
    var isFederation = role === 'national' || role === 'pref';
    showNav('home', true);
    showNav('ai-input', !isFederation);
    showNav('manual-input', !isFederation);
    showNav('expert-import', !isFederation);
    showNav('reports', true);
    showNav('monthly', true);
    showNav('ai-proposal', true);
    showNav('knowledge-search', true);
    showNav('accounts', true);
    showNav('knowledge', isFederation);

    var entrySection = document.getElementById('nav-section-entry');
    if (entrySection) entrySection.style.display = isFederation ? 'none' : '';
    var knowledgeItem = document.getElementById('nav-item-knowledge');
    if (knowledgeItem) knowledgeItem.style.display = isFederation ? '' : 'none';
  }

  function applyOrgRole(role) {
    // 組織名／ユーザーはログイン session（Init／localStorage）を優先。ロール切替デモでは色とフィルタのみ変える
    applySessionProfile();
    applyRoleMenuFallback(role);

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
    if ((location.hash || '').replace(/^#/, '') === 'monthly'
        && typeof window.__renderMonthly === 'function') {
      window.__renderMonthly();
      return;
    }
    location.hash = '#home';
  });
  applyOrgRole(roleSelect.value);
})();
