(function () {
  var row = document.getElementById('login-otp-row');
  var hidden = document.getElementById('login-otp-hidden');
  if (!row || !hidden) return;

  var boxes = Array.from(row.querySelectorAll('.login-otp-box'));

  function syncHidden() {
    hidden.value = boxes.map(function (b) { return b.value; }).join('');
  }

  boxes.forEach(function (box, index) {
    box.addEventListener('focus', function () { box.select(); });

    box.addEventListener('input', function () {
      box.value = box.value.replace(/\D/g, '').slice(-1);
      syncHidden();
      if (box.value && index < boxes.length - 1) {
        boxes[index + 1].focus();
      }
    });

    box.addEventListener('keydown', function (e) {
      if (e.key === 'Backspace' && !box.value && index > 0) {
        boxes[index - 1].focus();
      }
    });

    box.addEventListener('paste', function (e) {
      var pasted = (e.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '');
      if (!pasted) return;
      e.preventDefault();
      pasted.slice(0, boxes.length).split('').forEach(function (digit, i) {
        if (boxes[i]) boxes[i].value = digit;
      });
      syncHidden();
      var next = boxes[Math.min(pasted.length, boxes.length - 1)];
      if (next) next.focus();
    });
  });
})();
