(function () {
  // ExpertImportAPI を呼び出し、同一画面上でフォーム項目へ反映する
  function applyExpertImport(data) {
    // UI切替：専門家取込パネルを非表示、入力ステップを表示
    const detailGridEl = document.querySelector('.mi-detail-grid');
    if (detailGridEl) {
      detailGridEl.classList.remove('mi-detail-grid--import-pending');
      detailGridEl.classList.remove('mi-detail-grid--swapped');
    }
    const expertPanelsEl = document.getElementById('mi-expert-import-panels');
    if (expertPanelsEl) expertPanelsEl.style.display = 'none';
    const voiceCardEl = document.getElementById('mi-voice-card');
    if (voiceCardEl) voiceCardEl.style.display = 'none';
    const importStepsDropdownEl = document.getElementById('mi-import-steps-dropdown');
    if (importStepsDropdownEl) importStepsDropdownEl.style.display = '';
    const utilityLabelEl = document.getElementById('mi-utility-label');
    if (utilityLabelEl) utilityLabelEl.style.display = '';
    if (voiceCardEl) voiceCardEl.removeAttribute('open');
    if (importStepsDropdownEl) importStepsDropdownEl.setAttribute('open', '');
    const importStepsListEl = document.getElementById('mi-import-steps-content');
    const importStepsPanelEl = document.getElementById('mi-import-steps-panel');
    if (importStepsListEl && importStepsPanelEl) importStepsPanelEl.appendChild(importStepsListEl);

    // 帳票select
    const formSelect = document.getElementById('mi-form');
    if (formSelect) {
      formSelect.value = data.dragFormCode;
      formSelect.dispatchEvent(new Event('change', { bubbles: true }));
      if (typeof SelectWidth !== 'undefined') SelectWidth.fit(formSelect);
      if (typeof syncSelectPlaceholder === 'function') syncSelectPlaceholder(formSelect);
    }
    // 対応日
    const dateEl = document.getElementById('mi-date');
    if (dateEl) { dateEl.value = data.dragReportDate; dateEl.dispatchEvent(new Event('input')); }
    // 開始時刻
    const timeStartEl = document.getElementById('mi-time-start');
    if (timeStartEl) { timeStartEl.value = data.dragTimeStart; timeStartEl.dispatchEvent(new Event('input')); }
    // 終了時刻
    const timeEndEl = document.getElementById('mi-time-end');
    if (timeEndEl) { timeEndEl.value = data.dragTimeEnd; timeEndEl.dispatchEvent(new Event('input')); }
    // 支援テーマ
    document.querySelectorAll('.mi-theme-checkbox').forEach((cb) => {
      cb.checked = (cb.value === data.dragThemeCode);
      cb.dispatchEvent(new Event('change'));
    });
    // 内容（summary）
    const contentEl = document.getElementById('mi-content');
    if (contentEl) { contentEl.value = data.dragSummary; contentEl.dispatchEvent(new Event('input')); }
  }

  window.applyExpertImport = applyExpertImport;

  function importExpertReport(file, formCode) {
    if (!file) return;
    if (!window.ApiClient || typeof window.ApiClient.post !== 'function') {
      Toast.error('APIクライアントが利用できません');
      return;
    }
    window.ApiClient.post('./expertimportapi.do', {
      filename: file.name,
      formcode: formCode,
    }).then(function (res) {
      const data = (res && res.data) || {};
      if (data.e) { Toast.error(data.e); return; }
      applyExpertImport(data);
      Toast.success(file.name + ' を取り込みました');
    }).catch(function () {
      Toast.error('専門家報告の取り込みに失敗しました');
    });
  }

  function wirePanel(dropzoneId, fileInputId, formCode) {
    const dropzone = document.getElementById(dropzoneId);
    const fileInput = document.getElementById(fileInputId);
    if (!dropzone || !fileInput) return;

    function handleFile(file) {
      if (!file) return;
      importExpertReport(file, formCode);
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

  wirePanel('mi-g4-dropzone', 'mi-g4-file', 'G-4');
  wirePanel('mi-g5-dropzone', 'mi-g5-file', 'G-5');
})();
