(function () {

  const navToggleBtn = document.getElementById('nav-toggle-btn');

  function setNavOpen(open) {
    const isOpen = typeof open === 'boolean' ? open : !document.body.classList.contains('nav-open');
    document.body.classList.toggle('nav-open', isOpen);
    if (navToggleBtn) {
      navToggleBtn.textContent = isOpen ? '✕' : '☰';
      navToggleBtn.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
    }
  }

  const sidebarScrim = document.getElementById('sidebar-scrim');
  if (navToggleBtn) navToggleBtn.addEventListener('click', () => setNavOpen());
  if (sidebarScrim) sidebarScrim.addEventListener('click', () => setNavOpen(false));
})();
