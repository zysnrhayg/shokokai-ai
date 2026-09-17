function prefillFromHashQuery(hashQuery) {
  if (!hashQuery) return null;
  let params;
  try {
    params = new URLSearchParams(hashQuery);
  } catch (e) {
    return null;
  }
  const content = params.get('content');
  if (content == null || content === '') return null;
  const themesRaw = params.get('themes') || '';
  const themeCodes = themesRaw.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
  return {
    content: content,
    themeCodes: themeCodes,
    businessName: params.get('business_name') || '',
  };
}

function applyEntryScreen(screenId, hashQuery) {

  const entryForm = document.getElementById('mi-entry-form');
  if (entryForm) {

    entryForm.setAttribute('data-screen', screenId);

    entryForm.querySelectorAll('input, select, textarea, button').forEach((el) => { el.disabled = false; });
    entryForm.querySelectorAll('label.btn, label.import-zone, label.mi-expert-panel__dropzone').forEach((el) => {
      el.style.opacity = '';
      el.style.pointerEvents = '';
      el.style.cursor = '';
    });
    entryForm.reset();
    entryForm.querySelectorAll('.is-invalid').forEach((el) => el.classList.remove('is-invalid'));
    entryForm.querySelectorAll('.detail-row--invalid').forEach((el) => el.classList.remove('detail-row--invalid'));

    const consentCheckboxEl = document.getElementById('mi-voice-consent');
    if (consentCheckboxEl) consentCheckboxEl.dispatchEvent(new Event('change'));
    const transcriptDisplayResetEl = document.getElementById('mi-transcript-display');
    if (transcriptDisplayResetEl) transcriptDisplayResetEl.value = '';
    const expiryNoteResetEl = document.getElementById('mi-voice-expiry-note');
    if (expiryNoteResetEl) expiryNoteResetEl.textContent = '';
    if (typeof SelectWidth !== 'undefined') {
      SelectWidth.fit(document.getElementById('mi-staff-main'));
      SelectWidth.fit(document.getElementById('mi-staff-sub'));
      SelectWidth.fit(document.getElementById('mi-industry'));
    }
  }

  let prefill = null;
  if (['manual-input', 'ai-input', 'expert-import'].includes(screenId)) {
    if (window.__miPendingPrefill) {
      prefill = window.__miPendingPrefill;
      window.__miPendingPrefill = null;
    } else {
      prefill = prefillFromHashQuery(hashQuery);
    }
  }
  if (prefill) {
    const contentEl = document.getElementById('mi-content');
    if (contentEl) contentEl.value = prefill.content;
    if (prefill.themeCodes && prefill.themeCodes.length) {
      document.querySelectorAll('.mi-theme-checkbox').forEach((cb) => {
        cb.checked = prefill.themeCodes.includes(cb.value);
      });
    }
    if (prefill.businessName) {
      const jigyoshoEl = document.getElementById('mi-jigyosho');
      if (jigyoshoEl) jigyoshoEl.value = prefill.businessName;
    }

    if (prefill.formCode) {
      const formEl = document.getElementById('mi-form');
      if (formEl) {
        formEl.value = prefill.formCode;
        formEl.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
    if (prefill.reportDate) {
      const dateEl = document.getElementById('mi-date');
      if (dateEl) dateEl.value = prefill.reportDate;
    }
    if (prefill.timeStart) {
      const timeStartEl = document.getElementById('mi-time-start');
      if (timeStartEl) timeStartEl.value = prefill.timeStart;
    }
    if (prefill.timeEnd) {
      const timeEndEl = document.getElementById('mi-time-end');
      if (timeEndEl) timeEndEl.value = prefill.timeEnd;
    }

    const selectByOptionText = (selectEl, text) => {
      if (!selectEl || !text) return;
      const opt = Array.prototype.find.call(selectEl.options, (o) => o.textContent.trim() === text);
      if (opt) selectEl.value = opt.value;
    };
    selectByOptionText(document.getElementById('mi-staff-main'), prefill.staffMainName);
    selectByOptionText(document.getElementById('mi-staff-sub'), prefill.staffSubName);
    if (typeof SelectWidth !== 'undefined') {
      SelectWidth.fit(document.getElementById('mi-staff-main'));
      SelectWidth.fit(document.getElementById('mi-staff-sub'));
    }

    const entryFormEl = document.getElementById('mi-entry-form');
    if (prefill.readOnly && entryFormEl) {
      entryFormEl.querySelectorAll('input, select, textarea, button').forEach((el) => {
        if (el.id === 'mi-form-export-btn') return;
        el.disabled = true;
      });

      entryFormEl.querySelectorAll('label.btn, label.import-zone, label.mi-expert-panel__dropzone').forEach((el) => {
        el.style.opacity = '0.4';
        el.style.pointerEvents = 'none';
        el.style.cursor = 'default';
      });
      Toast.success('閲覧専用で表示しています（入力・登録はできません）');
    } else {
      Toast.success('報告書入力欄に反映しました');
    }
  }

  const SCREENS = {
    'ai-input': {
      title: '相談を受ける',
      subtitle: '相談内容を入力し、受付票を出力できます',
      cardTitle: '相談内容登録',
    },
    'manual-input': {
      title: '報告書を作る',
      subtitle: '対応内容を入力し、報告書を出力できます',
      cardTitle: '報告内容登録',

      defaultOpenPanel: 'history',

      historyLabel: '🕘 事業所に紐づく過去の報告履歴を表示します',
      historyNoun: '報告',
    },
    'expert-import': {
      title: '専門家の報告を取り込む',
      subtitle: '専門家から取得した報告書を取り込み登録できます',
      cardTitle: '報告内容登録',

      showExpertPanels: true,

      swapPanels: true,
      hideHistory: true,
    },
  };
  const screen = SCREENS[screenId] || SCREENS['ai-input'];

  const titleEl = document.getElementById('app-title');
  const subtitleEl = document.getElementById('app-subtitle');
  if (titleEl) titleEl.textContent = screen.title;
  if (subtitleEl) subtitleEl.textContent = screen.subtitle;

  const cardTitleEl = document.querySelector('#mi-detail-card .card-title');
  if (cardTitleEl && screen.cardTitle) cardTitleEl.textContent = screen.cardTitle;

  const historyLabelEl = document.getElementById('mi-history-label');
  const DEFAULT_HISTORY_LABEL = '🕘 事業所に紐づく過去の相談履歴を表示します';
  if (historyLabelEl) historyLabelEl.textContent = screen.historyLabel || DEFAULT_HISTORY_LABEL;

  window.__miHistoryNoun = screen.historyNoun || '相談';
  if (typeof updateHistoryVisibility === 'function') updateHistoryVisibility();

  const voiceCardEl = document.getElementById('mi-voice-card');
  const expertPanelsEl = document.getElementById('mi-expert-import-panels');
  if (voiceCardEl) voiceCardEl.style.display = screen.showExpertPanels ? 'none' : '';
  if (expertPanelsEl) expertPanelsEl.style.display = screen.showExpertPanels ? '' : 'none';

  const importStepsDropdownEl = document.getElementById('mi-import-steps-dropdown');
  if (importStepsDropdownEl) importStepsDropdownEl.style.display = 'none';
  const importStepsListEl = document.getElementById('mi-import-steps-content');
  const importStepsCardBodyEl = document.getElementById('mi-expert-steps-card-body');
  if (importStepsListEl && importStepsCardBodyEl && importStepsListEl.parentElement !== importStepsCardBodyEl) {
    importStepsCardBodyEl.prepend(importStepsListEl);
  }

  const detailGridEl = document.querySelector('.mi-detail-grid');
  if (detailGridEl) detailGridEl.classList.toggle('mi-detail-grid--swapped', !!screen.swapPanels);

  if (detailGridEl) detailGridEl.classList.toggle('mi-detail-grid--import-pending', !!screen.showExpertPanels);

  const expertStepsCardEl = document.querySelector('.mi-expert-steps');
  if (expertStepsCardEl) {
    expertStepsCardEl.style.minHeight = '';
    if (screen.showExpertPanels) {
      requestAnimationFrame(() => alignCardBottomToManualInput(expertStepsCardEl, false));
    }
  }
  const historyEl = document.getElementById('mi-history-dropdown');
  if (historyEl) historyEl.style.display = screen.hideHistory ? 'none' : '';
  const utilityLabelEl = document.getElementById('mi-utility-label');
  if (utilityLabelEl) utilityLabelEl.style.display = screen.showExpertPanels ? 'none' : '';

  const detailInfoEl = document.getElementById('mi-detail-info-dropdown');
  if (detailInfoEl) detailInfoEl.style.display = screen.showExpertPanels ? 'none' : '';

  if (voiceCardEl && historyEl) {
    if (screen.defaultOpenPanel === 'history') {
      voiceCardEl.removeAttribute('open');
      historyEl.setAttribute('open', '');
    } else {
      historyEl.removeAttribute('open');
      voiceCardEl.setAttribute('open', '');
    }
  }

  if (typeof window.__syncTranscriptDisplayHeight === 'function') {
    requestAnimationFrame(window.__syncTranscriptDisplayHeight);
  }

  const formSelect = document.getElementById('mi-form');
  if (formSelect) {
    const placeholderOpt = formSelect.querySelector('option[value=""]');
    const allowedValues = [];
    Array.from(formSelect.options).forEach((opt) => {
      if (!opt.value) return;
      const allowed = (opt.dataset.screens || '').split(',');
      const isAllowed = allowed.includes(screenId);
      opt.hidden = !isAllowed;
      opt.disabled = !isAllowed;
      if (isAllowed) allowedValues.push(opt.value);
    });

    if (placeholderOpt) {
      placeholderOpt.hidden = allowedValues.length === 1;
      placeholderOpt.disabled = allowedValues.length === 1;
    }
    if (allowedValues.length === 1) {
      formSelect.value = allowedValues[0];
    } else if (!allowedValues.includes(formSelect.value)) {
      formSelect.value = '';
    }

    if (typeof SelectWidth !== 'undefined') SelectWidth.fit(formSelect);
  }

  const importModal = document.getElementById('ei-import-modal');
  if (importModal && screen.showImportModal) importModal.classList.add('is-open');

  if (entryForm && typeof syncAllSelectPlaceholders === 'function') syncAllSelectPlaceholders(entryForm);

  const detailGridForAlign = document.querySelector('.mi-detail-grid');
  if (detailGridForAlign) detailGridForAlign.style.minHeight = '';

  if (screenId === 'ai-input') {
    const focusEl = document.getElementById('mi-time-start');
    if (focusEl) focusEl.focus();
  } else if (screenId === 'manual-input') {
    const focusEl = document.getElementById('mi-form');
    if (focusEl) focusEl.focus();
  }
}
