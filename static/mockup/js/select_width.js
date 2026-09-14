const SelectWidth = {
  _ctx: null,

  _ctx2() {
    if (!this._ctx) this._ctx = document.createElement('canvas').getContext('2d');
    return this._ctx;
  },

  fit(el) {
    if (!el || !el.options || !el.options.length) return;
    this._applySelectedWidth(el);
    if (!el.dataset.fitWired) {
      el.dataset.fitWired = '1';
      el.addEventListener('change', () => this._applySelectedWidth(el));
    }
  },

  _applySelectedWidth(el) {
    const cs = getComputedStyle(el);
    const ctx = this._ctx2();
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const opt = el.options[el.selectedIndex] || el.options[0];
    const w = ctx.measureText(opt.textContent || '').width;
    const chrome = (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0) + 28;
    el.style.width = Math.ceil(w + chrome) + 'px';
  },

  fitAll(root, selector) {
    root.querySelectorAll(selector || 'select.form-input--compact').forEach(el => this.fit(el));
  },

  fitChars(el, { half = 0, full = 0 } = {}) {
    if (!el) return;
    const cs = getComputedStyle(el);
    const ctx = this._ctx2();
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const halfWidth = ctx.measureText('0').width;
    const fullWidth = ctx.measureText('国').width;
    const borderX = (parseFloat(cs.borderLeftWidth) || 0) + (parseFloat(cs.borderRightWidth) || 0);
    const isSelect = el.tagName === 'SELECT';
    const chrome = (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0) + borderX + (isSelect ? 28 : 6);
    el.style.width = Math.ceil(halfWidth * half + fullWidth * full + chrome) + 'px';
  },

  fitPlaceholder(el, extraPx) {
    if (!el || !el.placeholder) return;
    const cs = getComputedStyle(el);
    const ctx = this._ctx2();
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const w = ctx.measureText(el.placeholder).width;
    const borderX = (parseFloat(cs.borderLeftWidth) || 0) + (parseFloat(cs.borderRightWidth) || 0);
    const chrome = (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0) + borderX + (extraPx == null ? 6 : extraPx);
    el.style.width = Math.ceil(w + chrome) + 'px';
  }
};
