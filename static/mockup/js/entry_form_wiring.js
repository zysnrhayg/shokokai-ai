(function () {

  SelectWidth.fitChars(document.getElementById('mi-date'), { half: 12 });
  SelectWidth.fitChars(document.getElementById('mi-time-start'), { half: 7 });
  SelectWidth.fitChars(document.getElementById('mi-time-end'), { half: 7 });
  SelectWidth.fitChars(document.getElementById('mi-jigyosho'), { full: 20 });

  SelectWidth.fitChars(document.getElementById('mi-content'), { full: 40 });
  SelectWidth.fitChars(document.getElementById('mi-jigyosha'), { half: 10, full: 2 });
  SelectWidth.fit(document.getElementById('mi-staff-main'));
  SelectWidth.fit(document.getElementById('mi-staff-sub'));

  SelectWidth.fit(document.getElementById('mi-form'));
  SelectWidth.fit(document.getElementById('mi-industry'));

  {
    const attachmentsEl = document.getElementById('mi-attachments');
    const attachmentsListEl = document.getElementById('mi-attachments-list');
    if (attachmentsEl && attachmentsListEl) {
      attachmentsEl.addEventListener('change', () => {
        const files = Array.from(attachmentsEl.files || []);
        attachmentsListEl.textContent = files.length
          ? `選択中：${files.map(f => f.name).join('、')}`
          : '';
      });
    }
  }

  {
    const timeStartEl = document.getElementById('mi-time-start');
    if (timeStartEl && !timeStartEl.value) {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      timeStartEl.value = `${hh}:${mm}`;
    }
  }

  {
    const dateEl = document.getElementById('mi-date');
    const noticeEl = document.getElementById('mi-date-prev-month-notice');
    if (dateEl && noticeEl) {
      const updateDateNotice = () => {
        if (!dateEl.value) { noticeEl.style.display = 'none'; return; }
        const [y, m] = dateEl.value.split('-').map(Number);
        const now = new Date();
        const prevMonthDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const isPrevMonth = y === prevMonthDate.getFullYear() && m === prevMonthDate.getMonth() + 1;
        noticeEl.style.display = isPrevMonth ? '' : 'none';
      };
      dateEl.addEventListener('change', updateDateNotice);
      updateDateNotice();
    }
  }

  function aiFormat(text) {
    let t = (text || '').trim();
    if (!t) return t;
    t = t.replace(/(えーと|えっと|あの、|うーん、|まあ、)/g, '');
    t = t.replace(/、\s*/g, '、');
    t = t.replace(/。\s*/g, '。\n');
    return t.trim();
  }

  function aiSummarize(text) {
    const t = (text || '').trim();
    if (!t) return '';
    const sentences = t.split('。').map(s => s.trim()).filter(Boolean);
    return sentences.slice(0, 2).join('。') + (sentences.length ? '。' : '');
  }

  const contentEl = document.getElementById('mi-content');

  const csrfTokenEl = document.querySelector('input[name="csrf_token"]');
  const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

  const contentFormatBtn = document.getElementById('mi-content-ai-format');
  if (contentFormatBtn && contentEl) {
    contentFormatBtn.addEventListener('click', () => {
      if (!contentEl.value.trim()) {
        Toast.error('内容が未入力のため整形できません');
        return;
      }
      const before = contentEl.value;
      contentEl.value = aiFormat(contentEl.value);
      Toast.success('内容の誤字脱字等をAIで整形しました');
      logAiUsage('/manual-input/log-usage', csrfToken, 'manual_input.text_format', before, contentEl.value);
    });
  }

  const overviewAiBtn = document.getElementById('mi-overview-ai-btn');
  const overviewEl = document.getElementById('mi-overview');
  if (overviewAiBtn && contentEl && overviewEl) {
    overviewAiBtn.addEventListener('click', () => {
      const content = contentEl.value.trim();
      if (!content) {
        Toast.error('内容が未入力のため要約できません');
        return;
      }
      overviewEl.value = aiSummarize(content);
      Toast.success('内容をAIで要約し、概要欄に反映しました');
      logAiUsage('/manual-input/log-usage', csrfToken, 'manual_input.summarize', content, overviewEl.value);
    });
  }

  const exportBtn = document.getElementById('mi-form-export-btn');
  const formSelect = document.getElementById('mi-form');
  if (exportBtn && formSelect) {
    exportBtn.addEventListener('click', () => {
      if (!formSelect.value) {
        Toast.error('帳票を選択してください');
        return;
      }
      const label = formSelect.options[formSelect.selectedIndex].textContent;
      Toast.success(`${label}を出力しました`);
    });
  }

  const expertImportBtn = document.getElementById('mi-expert-import-btn');
  const expertImportModal = document.getElementById('ei-import-modal');
  if (formSelect && expertImportBtn && expertImportModal) {
    formSelect.addEventListener('change', () => {
      const isImportTarget = formSelect.value === 'G-4' || formSelect.value === 'G-5';
      expertImportBtn.style.display = isImportTarget ? '' : 'none';
      if (isImportTarget) expertImportModal.classList.add('is-open');
    });
    expertImportBtn.addEventListener('click', () => expertImportModal.classList.add('is-open'));
  }

  const extraFieldRows = document.querySelectorAll('.mi-extra-field');
  if (formSelect && extraFieldRows.length) {
    formSelect.addEventListener('change', () => {
      const code = formSelect.value.toLowerCase();
      extraFieldRows.forEach((row) => {
        const matches = code && row.classList.contains('mi-form-' + code);
        row.classList.toggle('mi-extra-field--hidden', !matches);
      });
    });
  }

  const REQUIRED_FIELDS = [
    { el: formSelect, label: '帳票' },
    { el: document.getElementById('mi-date'), label: '対応日時' },
    { el: document.getElementById('mi-time-start'), label: '対応日時' },
    { el: document.getElementById('mi-time-end'), label: '対応日時' },
    { el: document.getElementById('mi-staff-main'), label: '担当（主／副）' },
    { el: document.getElementById('mi-jigyosho'), label: '事業所／担当者' },
    { el: document.getElementById('mi-jigyosha'), label: '事業所／担当者' },
    { el: document.getElementById('mi-industry'), label: '業種' },
    { el: contentEl, label: '内容' },
  ].filter((f) => f.el);
  const themeCheckboxes = document.querySelectorAll('.mi-theme-checkbox');

  const themeGrid = document.getElementById('mi-theme-select') || document.querySelector('.checkbox-grid');

  {
    const actionsEl = document.getElementById('mi-form-actions');

    const syncContentActionsWidth = () => {
      if (!contentEl || !actionsEl) return;
      actionsEl.style.marginLeft = '0px';
      const contentRect = contentEl.getBoundingClientRect();
      const actionsLeft = actionsEl.getBoundingClientRect().left;
      const marginLeft = contentRect.left - actionsLeft;
      if (marginLeft > 0) actionsEl.style.marginLeft = marginLeft + 'px';
      const width = contentRect.right - contentRect.left;
      if (width > 0) actionsEl.style.width = width + 'px';
    };
    if (actionsEl) {
      if (window.ResizeObserver) {
        new ResizeObserver(syncContentActionsWidth).observe(contentEl);
      } else {
        window.addEventListener('resize', debounce(syncContentActionsWidth, 150));
      }
      syncContentActionsWidth();
    }
  }

  function clearInvalid(el) {
    el.classList.remove('is-invalid');
    const row = el.closest('.detail-row');
    if (row) row.classList.remove('detail-row--invalid');
  }
  function markInvalid(el) {
    el.classList.add('is-invalid');
    const row = el.closest('.detail-row');
    if (row) row.classList.add('detail-row--invalid');
  }

  REQUIRED_FIELDS.forEach(({ el }) => {
    el.addEventListener(el.tagName === 'SELECT' ? 'change' : 'input', () => {
      if (el.value.trim()) clearInvalid(el);
    });
  });
  function setThemeInvalid(invalid) {
    if (!themeGrid) return;
    themeGrid.classList.toggle('is-invalid', invalid);
    const row = themeGrid.closest('.detail-row');
    if (row) row.classList.toggle('detail-row--invalid', invalid);
  }
  themeCheckboxes.forEach((cb) => {
    cb.addEventListener('change', () => {
      if ([...themeCheckboxes].some((c) => c.checked)) setThemeInvalid(false);
    });
  });

  const themeTrigger = document.getElementById('mi-theme-trigger');
  const themePopover = document.getElementById('mi-theme-popover');
  const themeTagsEl = document.getElementById('mi-theme-tags');
  if (themeTrigger && themePopover) {
    themeTrigger.addEventListener('click', (e) => {
      e.stopPropagation();
      themePopover.classList.toggle('is-open');
    });
    document.addEventListener('click', (e) => {
      if (themePopover.classList.contains('is-open') && themeGrid && !themeGrid.contains(e.target)) {
        themePopover.classList.remove('is-open');
      }
    });
  }

  function renderThemeTags() {
    if (!themeTagsEl) return;
    const checked = [...themeCheckboxes].filter((c) => c.checked);
    themeTagsEl.innerHTML = '';
    checked.forEach((cb) => {
      const label = cb.dataset.label || cb.value;
      const tag = document.createElement('span');
      tag.className = 'mi-theme-tag';
      tag.textContent = label;
      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.textContent = '×';
      removeBtn.setAttribute('aria-label', `${label}を削除`);
      removeBtn.addEventListener('click', () => {
        cb.checked = false;
        renderThemeTags();
      });
      tag.appendChild(removeBtn);
      themeTagsEl.appendChild(tag);
    });
    if (themeTrigger) {
      themeTrigger.textContent = checked.length ? `🏷 支援テーマを選択（${checked.length}件選択中）` : '🏷 支援テーマを選択';
    }
  }
  if (themeTagsEl) {
    themeCheckboxes.forEach((cb) => cb.addEventListener('change', renderThemeTags));
    renderThemeTags();
  }

  {
    const miForm = document.querySelector('#mi-submit')?.form;
    if (miForm) {
      miForm.addEventListener('submit', (e) => {
        const isDraft = e.submitter && e.submitter.value === 'draft';

        if (isDraft) {
          e.preventDefault();
          Toast.success('下書きとして保存しました');
          return;
        }
        if (!isDraft) {

          if (overviewEl && contentEl && !overviewEl.value.trim() && contentEl.value.trim()) {
            overviewEl.value = aiSummarize(contentEl.value);
          }
          const missingLabels = [];
          REQUIRED_FIELDS.forEach(({ el, label }) => {
            if (el.value.trim()) {
              clearInvalid(el);
            } else {
              markInvalid(el);
              if (!missingLabels.includes(label)) missingLabels.push(label);
            }
          });
          if (themeCheckboxes.length) {
            const hasTheme = [...themeCheckboxes].some((c) => c.checked);
            setThemeInvalid(!hasTheme);
            if (!hasTheme) missingLabels.push('支援テーマ');
          }
          if (missingLabels.length) {
            e.preventDefault();
            Toast.error(`必須項目（※）が未入力です。ご確認ください（未入力: ${missingLabels.join('、')}）`);
            const firstInvalid = document.querySelector('.is-invalid');
            if (firstInvalid) firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
          }
        }
        setTimeout(() => {
          miForm.querySelectorAll('button[type="submit"]').forEach((btn) => { btn.disabled = true; });
        }, 0);
      });
    }
  }

  const voiceCard = document.getElementById('mi-voice-card');

  const DEFAULT_TIMER_SECONDS = (parseInt(voiceCard && voiceCard.dataset.defaultMinutes, 10) || 30) * 60;
  const MAX_TIMER_SECONDS = 3600;
  const EXTEND_SECONDS = 1800;

  const detailCard = document.getElementById('mi-detail-card');
  const consentCheckbox = document.getElementById('mi-voice-consent');
  const voiceBtn = document.getElementById('mi-voice-btn');
  const playBtn = document.getElementById('mi-play-btn');
  const uploadLabel = document.getElementById('mi-upload-label');
  const uploadInput = document.getElementById('mi-audio-upload');
  const extendBtn = document.getElementById('mi-extend-btn');
  const timerDisplay = document.getElementById('mi-timer-display');
  const transcriptEl = document.getElementById('mi-transcript');

  const transcriptDisplayEl = document.getElementById('mi-transcript-display');

  const applyTranscriptDisplayBtn = document.getElementById('mi-transcript-apply-btn');
  const aiFormatVoiceBtn = document.getElementById('mi-ai-format');
  const insertContentBtn = document.getElementById('mi-insert-content');
  const audioPlayer = document.getElementById('mi-audio-player');
  const maximizeBtn = document.getElementById('mi-voice-maximize');
  const expiryNote = document.getElementById('mi-voice-expiry-note');
  const voiceBtnHint = document.getElementById('mi-voice-btn-hint');

  if (voiceCard) {
    let audioBlobUrl = null;
    let timerTotal = DEFAULT_TIMER_SECONDS;
    let timerRemaining = DEFAULT_TIMER_SECONDS;
    let voiceMaximized = false;

    function updateTimerDisplay() {
      const mm = Math.floor(timerRemaining / 60);
      const ss = timerRemaining % 60;
      timerDisplay.textContent = '残り時間 ' + mm + ':' + String(ss).padStart(2, '0');
      timerDisplay.classList.toggle('mi-timer--warning', timerRemaining <= 300);
      if (extendBtn) extendBtn.disabled = !consentCheckbox.checked || timerTotal >= MAX_TIMER_SECONDS;
    }

    function setControlsEnabled(enabled) {
      voiceBtn.disabled = !enabled;

      playBtn.disabled = !enabled;
      uploadInput.disabled = !enabled;
      uploadLabel.style.opacity = enabled ? '' : '0.4';
      uploadLabel.style.pointerEvents = enabled ? '' : 'none';
      extendBtn.disabled = !enabled || timerTotal >= MAX_TIMER_SECONDS;
      if (transcriptEl) transcriptEl.disabled = !enabled;
      if (aiFormatVoiceBtn) aiFormatVoiceBtn.disabled = !enabled;
      if (insertContentBtn) insertContentBtn.disabled = !enabled;
      if (applyTranscriptDisplayBtn) applyTranscriptDisplayBtn.disabled = !enabled;

      if (voiceBtnHint) voiceBtnHint.style.display = enabled ? 'none' : '';
    }

    consentCheckbox.addEventListener('change', () => {
      if (!consentCheckbox.checked) stopRecording('consent-revoked');
      setControlsEnabled(consentCheckbox.checked);
    });

    const DUMMY_TRANSCRIPT = '（デモ音声入力）本日は資金繰りについてご相談を受けました。売上減少に伴う運転資金の確保が課題とのことで、日本政策金融公庫の融資制度をご案内しました。';
    let recordTimerId = null;

    function setVoiceBtnLabel(text) {
      const labelEl = voiceBtn.querySelector('.mi-voice-btn-square__label');
      if (labelEl) labelEl.textContent = text; else voiceBtn.textContent = text;
    }

    function stopRecording(reason) {
      if (recordTimerId === null) return;
      clearInterval(recordTimerId);
      recordTimerId = null;
      setVoiceBtnLabel('音声入力');
      voiceBtn.classList.remove('is-recording');
      if (reason === 'consent-revoked') {
        Toast.error('同意が解除されたため録音を停止しました');
        return;
      }

      if (transcriptEl) transcriptEl.value = DUMMY_TRANSCRIPT;

      if (transcriptDisplayEl) {
        transcriptDisplayEl.value = DUMMY_TRANSCRIPT;
        transcriptDisplayEl.readOnly = false;
      }

      if (expiryNote) {
        const deleteDate = new Date();
        deleteDate.setDate(deleteDate.getDate() + 30);
        expiryNote.textContent = `音声ファイルの削除予定日: ${formatDate(deleteDate, '/')}（録音した日から30日後に自動的に削除されます）`;
      }
      Toast.success(reason === 'timeout' ? '録音時間の上限に達したため停止し、文字起こし結果を反映しました' : '録音を停止し、文字起こし結果を反映しました');
    }

    voiceBtn.addEventListener('click', () => {
      if (recordTimerId !== null) {
        stopRecording('manual');
        return;
      }
      if (timerRemaining <= 0) {
        Toast.error('残り時間がありません。延長してください');
        return;
      }
      setVoiceBtnLabel('⏹ 停止');
      voiceBtn.classList.add('is-recording');
      Toast.success('録音を開始しました（デモ動作のため実際の音声は録音されません）');
      recordTimerId = setInterval(() => {
        timerRemaining--;
        updateTimerDisplay();
        if (timerRemaining <= 0) stopRecording('timeout');
      }, 1000);
    });

    uploadInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;
      if (audioBlobUrl) URL.revokeObjectURL(audioBlobUrl);
      audioBlobUrl = URL.createObjectURL(file);
      playBtn.disabled = !consentCheckbox.checked;
      const deleteDate = new Date();
      deleteDate.setMonth(deleteDate.getMonth() + 1);
      expiryNote.textContent = `音声ファイルの削除予定日: ${formatDate(deleteDate, '/')}（作成・アップロード日から1か月後に自動的に削除されます）`;
      Toast.success('音声ファイルをアップロードしました');
    });

    playBtn.addEventListener('click', () => {
      if (!audioBlobUrl) {
        Toast.error('この録音はデモ動作のため実際の音声データがありません（アップロードした音声のみ再生できます）');
        return;
      }
      audioPlayer.src = audioBlobUrl;
      audioPlayer.style.display = '';
      audioPlayer.play();
    });

    extendBtn.addEventListener('click', () => {
      if (timerTotal >= MAX_TIMER_SECONDS) return;
      const addSeconds = Math.min(EXTEND_SECONDS, MAX_TIMER_SECONDS - timerTotal);
      timerTotal += addSeconds;
      timerRemaining += addSeconds;
      Toast.success('30分延長しました');
      updateTimerDisplay();
    });

    if (aiFormatVoiceBtn && transcriptEl) {
      aiFormatVoiceBtn.addEventListener('click', () => {
        const before = transcriptEl.value;
        transcriptEl.value = aiFormat(transcriptEl.value);
        Toast.success('AIで文章を整形しました');
        logAiUsage('/manual-input/log-usage', csrfToken, 'manual_input.text_format', before, transcriptEl.value);
      });
    }

    if (insertContentBtn && transcriptEl) {
      insertContentBtn.addEventListener('click', () => {
        if (contentEl) contentEl.value = transcriptEl.value;
        Toast.success('内容欄に反映しました');
      });
    }

    if (applyTranscriptDisplayBtn && transcriptDisplayEl && contentEl) {
      applyTranscriptDisplayBtn.addEventListener('click', () => {
        if (!transcriptDisplayEl.value.trim()) {
          Toast.error('文字起こし結果がないため転記できません');
          return;
        }
        contentEl.value = contentEl.value.trim()
          ? contentEl.value.replace(/\n*$/, '\n') + transcriptDisplayEl.value
          : transcriptDisplayEl.value;
        Toast.success('内容欄に追記しました');
      });
    }

    function setVoiceMaximized(maximized) {
      voiceMaximized = maximized;
      if (voiceMaximized) {
        const voiceRect = voiceCard.getBoundingClientRect();
        const detailRect = detailCard.getBoundingClientRect();
        const width = voiceRect.right - detailRect.left;
        const height = voiceRect.bottom - detailRect.top;

        voiceCard.style.position = 'fixed';
        voiceCard.style.top = detailRect.top + 'px';
        voiceCard.style.left = detailRect.left + 'px';
        voiceCard.style.width = width + 'px';
        voiceCard.style.height = height + 'px';
        voiceCard.style.overflowY = 'auto';
        voiceCard.classList.add('is-maximized');
        if (maximizeBtn) { maximizeBtn.textContent = '⤡ 縮小'; maximizeBtn.title = '縮小'; }
      } else {
        voiceCard.style.position = '';
        voiceCard.style.top = '';
        voiceCard.style.left = '';
        voiceCard.style.width = '';
        voiceCard.style.height = '';
        voiceCard.style.overflowY = '';
        voiceCard.classList.remove('is-maximized');
        if (maximizeBtn) { maximizeBtn.textContent = '⛶ 最大化'; maximizeBtn.title = '最大化'; }
      }
    }

    if (maximizeBtn) maximizeBtn.addEventListener('click', () => setVoiceMaximized(!voiceMaximized));

    updateTimerDisplay();

    if (voiceCard.dataset.startMaximized === 'true') {
      requestAnimationFrame(() => setVoiceMaximized(true));
    }

  }
})();
