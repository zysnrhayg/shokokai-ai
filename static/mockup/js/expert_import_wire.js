(function () {
  function todayStr() { return formatDate(new Date()); }

  function wirePanel(dropzoneId, fileInputId, formCode, themeCode) {
    const dropzone = document.getElementById(dropzoneId);
    const fileInput = document.getElementById(fileInputId);
    if (!dropzone || !fileInput) return;

    function handleFile(file) {
      if (!file) return;
      Toast.success(`${file.name} を取り込みました`);
      finishExpertImport(formCode, themeCode);
    }

    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('is-dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('is-dragover'));
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('is-dragover');
      handleFile(e.dataTransfer.files[0]);
    });
  }

  wirePanel('mi-g4-dropzone', 'mi-g4-file', 'G-4', 'labor');
  wirePanel('mi-g5-dropzone', 'mi-g5-file', 'G-5', 'invoice');
})();
