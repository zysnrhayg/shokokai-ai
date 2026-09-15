const Toast = {

  _container() {
    var container = document.getElementById('toast-container');
    if (container) return container;
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
  },

  show(message, type) {
    const container = this._container();
    if (!container) {
      window.alert(message || '');
      return;
    }

    const el = document.createElement('div');
    el.className = 'toast toast--' + (type || 'success');

    const icon = document.createElement('span');
    icon.className = 'toast__icon';
    icon.textContent = type === 'error' ? '⚠️' : '✓';

    const text = document.createElement('span');
    text.className = 'toast__text';
    text.textContent = message;

    el.appendChild(icon);
    el.appendChild(text);
    container.appendChild(el);

    requestAnimationFrame(() => el.classList.add('is-visible'));

    setTimeout(() => {
      el.classList.remove('is-visible');
      setTimeout(() => el.remove(), 250);
    }, 3200);
  },

  success(message) {
    this.show(message || '登録しました', 'success');
  },

  error(message) {
    this.show(message || 'エラーが発生しました。入力内容をご確認ください', 'error');
  }
};
