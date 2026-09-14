function updateHistoryVisibility() {
  const jigyoshoEl = document.getElementById('mi-jigyosho');
  const emptyEl = document.getElementById('mi-history-empty');
  const stripEl = document.getElementById('mi-history-strip');
  if (!jigyoshoEl || !emptyEl || !stripEl) return;
  const hasBusiness = !!jigyoshoEl.value.trim();
  const noun = window.__miHistoryNoun || '相談';
  emptyEl.textContent = `事業所に紐づく${noun}履歴はありません。`;
  emptyEl.style.display = hasBusiness ? 'none' : '';
  stripEl.style.display = hasBusiness ? '' : 'none';
}
(function () {
  const jigyoshoEl = document.getElementById('mi-jigyosho');

  if (jigyoshoEl) jigyoshoEl.addEventListener('input', updateHistoryVisibility);
  updateHistoryVisibility();
})();
