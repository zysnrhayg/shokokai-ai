(function () {
  var input = document.getElementById('mi-jigyosho');
  var dropdown = document.getElementById('mi-jigyosho-dropdown');
  if (!input || !dropdown) return;

  var SAMPLE_NAMES = [
    '株式会社北海道フーズ', '有限会社さっぽろ工務店', '道央運送株式会社',
    '北見電機株式会社', '有限会社函館水産', '旭川商事株式会社',
  ];

  function render(matches) {
    dropdown.innerHTML = '';
    if (!matches.length) {
      var empty = document.createElement('div');
      empty.className = 'mi-autocomplete__item mi-autocomplete__item--empty';
      empty.textContent = '候補がありません';
      dropdown.appendChild(empty);
      return;
    }
    matches.forEach(function (name) {
      var item = document.createElement('div');
      item.className = 'mi-autocomplete__item';
      item.textContent = name;
      item.addEventListener('mousedown', function (e) {
        e.preventDefault();
        input.value = name;
        close();

        if (typeof updateHistoryVisibility === 'function') updateHistoryVisibility();
      });
      dropdown.appendChild(item);
    });
  }

  function close() { dropdown.classList.remove('is-open'); }

  function update() {
    var q = input.value.trim();
    if (!q) { close(); return; }
    var matches = SAMPLE_NAMES.filter(function (name) { return name.indexOf(q) !== -1; });
    render(matches);
    dropdown.classList.add('is-open');
  }

  input.addEventListener('input', update);
  input.addEventListener('focus', update);
  input.addEventListener('blur', close);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      close();
    }
  });
})();
