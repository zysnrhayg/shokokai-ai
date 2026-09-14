(function () {
  const modal = document.getElementById('ei-import-modal');
  const fileInput = document.getElementById('ei-file');
  const dropZone = document.getElementById('ei-drop-zone');
  const filenameEl = document.getElementById('ei-filename');
  const submitBtn = document.getElementById('ei-submit');
  const closeBtn = document.getElementById('ei-modal-close');
  if (!fileInput || !dropZone || !submitBtn) return;

  const close = () => { if (modal) modal.classList.remove('is-open'); };
  if (closeBtn) closeBtn.addEventListener('click', close);
  if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) close(); });

  let selectedFile = null;

  function setFile(file) {
    selectedFile = file || null;
    filenameEl.textContent = selectedFile ? selectedFile.name : '未選択（様式はファイル名から自動判定します）';
  }

  fileInput.addEventListener('change', (e) => setFile(e.target.files[0]));

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('is-dragover');
  });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('is-dragover'));
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('is-dragover');
    setFile(e.dataTransfer.files[0]);
  });

  function detectFormCode(fileName) {
    const name = fileName.toLowerCase();
    if (name.includes('g-4') || name.includes('g4')) return 'G-4';
    if (name.includes('g-5') || name.includes('g5')) return 'G-5';
    return null;
  }

  function todayStr() {
    return formatDate(new Date());
  }

  submitBtn.addEventListener('click', () => {
    if (!selectedFile) {
      Toast.error('Excelファイルを選択してください');
      return;
    }

    const formCode = detectFormCode(selectedFile.name);
    const themeCode = formCode === 'G-5' ? 'invoice' : 'labor';
    const summary = `（${selectedFile.name} を取り込みました。内容をご確認のうえ入力してください）`;

    const params = new URLSearchParams({
      date: todayStr(),
      time_start: '10:00',
      time_end: '11:00',
      theme: themeCode,
      summary,
    });
    if (formCode) params.set('form', formCode);
    else Toast.error('ファイル名から様式を自動判定できませんでした。帳票を選択してください');

    window.location.href = '/manual-input?' + params.toString();
  });
})();
