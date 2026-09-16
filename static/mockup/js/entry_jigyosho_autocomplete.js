(function () {
  var input = document.getElementById('mi-jigyosho');
  var dropdown = document.getElementById('mi-jigyosho-dropdown');
  if (!input || !dropdown) return;

  // サンプル事業所名（静的データ）
  var SAMPLE_NAMES = [
    '村上雑貨店',
    '長谷川工務店',
    '佐藤農園',
    '旅館いとう',
    '山本建材',
    '田中運送',
    '鈴木商店',
    '高橋印刷'
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
        input.dispatchEvent(new Event('input'));
      });
      dropdown.appendChild(item);
    });
  }

  function close() { dropdown.classList.remove('is-open'); }

  function update() {
    var q = input.value.trim();
    if (!q) { close(); return; }
    var matches = SAMPLE_NAMES.filter(function (n) {
      return n.indexOf(q) !== -1;
    });
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
