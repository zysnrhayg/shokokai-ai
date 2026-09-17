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
    filenameEl.textContent = selectedFile ? selectedFile.name : '未選択';
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

  submitBtn.addEventListener('click', () => {
    if (!selectedFile) {
      Toast.error('Excelファイルを選択してください');
      return;
    }

    // 帳票select（mi-form）の選択値から様式コードを取得する
    const formSelect = document.getElementById('mi-form');
    const formCode = formSelect ? formSelect.value : '';
    if (formCode !== 'G-4' && formCode !== 'G-5') {
      Toast.error('帳票で G-4 または G-5 を選択してください');
      return;
    }

    if (!window.ApiClient || typeof window.ApiClient.post !== 'function') {
      Toast.error('APIクライアントが利用できません');
      return;
    }

    // ExpertImportAPI を呼び出す
    window.ApiClient.post('./expertimportapi.do', {
      filename: selectedFile.name,
      formcode: formCode,
    }).then((res) => {
      const data = (res && res.data) || {};
      if (data.e) { Toast.error(data.e); return; }
      close();
      // 同一画面上でフォーム項目へ反映する
      if (typeof window.applyExpertImport === 'function') {
        window.applyExpertImport(data);
      }
      Toast.success(selectedFile.name + ' を取り込みました');
    }).catch(() => Toast.error('専門家報告の取り込みに失敗しました'));
  });
})();
