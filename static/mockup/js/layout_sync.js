(function () {
  const brandGroup = document.querySelector('.sidebar-brand-group');
  const topBar = document.querySelector('.top-bar');
  if (!brandGroup || !topBar) return;

  function syncTopBarHeight() {
    topBar.style.height = brandGroup.getBoundingClientRect().height + 'px';
  }

  syncTopBarHeight();
  window.addEventListener('resize', syncTopBarHeight);

  window.syncTopBarHeight = syncTopBarHeight;

  function watchDevicePixelRatioChange() {
    const mql = matchMedia(`(resolution: ${window.devicePixelRatio}dppx)`);
    mql.addEventListener('change', () => {
      syncTopBarHeight();
      watchDevicePixelRatioChange();
    }, { once: true });
  }
  watchDevicePixelRatioChange();
})();
