(function () {

  // ==========================================================================
  // 傾聴内容変換AI画面の配線（実データ版）
  // 各ボタンは *.do API（バックエンド）と接続し、DBの実データを表示・登録する。
  // ==========================================================================

  // 下書き保存で採番されたreport_id（帳票出力・既存下書きの更新に使用する）
  var state = { lastDraftReportId: '' };

  // JSON文字列／配列を安全にパースする共通関数
  function parseJson(raw, fallback) {
    if (raw == null || raw === '') return fallback;
    if (Array.isArray(raw)) return raw;
    if (typeof raw === 'string') {
      try { return JSON.parse(raw); } catch (e) { return fallback; }
    }
    return fallback;
  }

  // *.do API呼び出し共通関数（レスポンスのdata部分を返す）
  function callApi(url, body) {
    if (window.ApiClient && typeof window.ApiClient.post === 'function') {
      return window.ApiClient.post(url, body).then(function (res) {
        return (res && res.data) || {};
      });
    }
    return Promise.reject(new Error('ApiClient not found'));
  }

  // 添付ファイル付きでmultipart送信する（formnewsaveapi.do／draftsaveapi.do用）
  function callApiMultipart(url, formData) {
    if (window.ApiClient && typeof window.ApiClient.postMultipart === 'function') {
      return window.ApiClient.postMultipart(url, formData).then(function (res) {
        return (res && res.data) || {};
      });
    }
    return Promise.reject(new Error('ApiClient not found'));
  }

  // ファイル選択欄（mi-attachments）から選択中のファイル一覧を取得する
  function getSelectedAttachments() {
    var el = document.getElementById('mi-attachments');
    return el ? Array.from(el.files || []) : [];
  }

  // 保存成功後にファイル選択欄をクリアする（再保存時の二重登録防止）
  function clearSelectedAttachments() {
    var el = document.getElementById('mi-attachments');
    var listEl = document.getElementById('mi-attachments-list');
    if (el) el.value = '';
    if (listEl) listEl.textContent = '';
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value : '';
  }

  function setVal(id, value) {
    var el = document.getElementById(id);
    if (el) el.value = value == null ? '' : value;
  }

  // 担当selectから選択中の職員名（shokuin_kj）を取得する
  function selectedText(id) {
    var el = document.getElementById(id);
    if (!el || el.selectedIndex < 0) return '';
    return el.options[el.selectedIndex].textContent || '';
  }

  // 職員名と一致するoptionを選択状態にする
  function selectByText(id, text) {
    var el = document.getElementById(id);
    if (!el || !text) return;
    Array.prototype.forEach.call(el.options, function (opt) {
      if (opt.textContent === text) el.value = opt.value;
    });
  }

  // ==========================================================================
  // 画面初期表示（AiInputInitAPI）：帳票・支援テーマ・担当者を実データで再構築する
  // ==========================================================================
  function applyInitData(forms, themes, staff) {

    // 帳票select（mi-form）をmst_formの実データで再構築する（data-screens属性は既存値を維持）
    var formSelect = document.getElementById('mi-form');
    if (formSelect && forms.length) {
      var screensMap = {};
      Array.prototype.forEach.call(formSelect.options, function (opt) {
        if (opt.value) screensMap[opt.value] = opt.getAttribute('data-screens') || '';
      });
      var placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = '帳票を選択してください';
      formSelect.innerHTML = '';
      formSelect.appendChild(placeholder);
      forms.forEach(function (f) {
        var opt = document.createElement('option');
        opt.value = f.form_code || '';
        opt.textContent = f.full_label || f.short_label || f.form_code || '';
        if (screensMap[f.form_code]) opt.setAttribute('data-screens', screensMap[f.form_code]);
        formSelect.appendChild(opt);
      });
    }

    // 支援テーマcheckbox（mst_themeの実データ）で再構築する
    if (themes.length) {
      var grid = document.getElementById('mi-theme-select') || document.querySelector('.checkbox-grid');
      if (grid) {
        grid.innerHTML = '';
        themes.forEach(function (t) {
          var label = document.createElement('label');
          var cb = document.createElement('input');
          cb.type = 'checkbox';
          cb.className = 'mi-theme-checkbox';
          cb.name = 'theme_codes';
          cb.value = t.theme_code || '';
          cb.dataset.label = t.label || '';
          label.appendChild(cb);
          label.appendChild(document.createTextNode(' ' + (t.label || t.theme_code || '')));
          grid.appendChild(label);
        });
      }
    }

    // 担当select（主／副）をmst_user_accountの実データで再構築する
    if (staff.length) {
      ['mi-staff-main', 'mi-staff-sub'].forEach(function (id, idx) {
        var sel = document.getElementById(id);
        if (!sel) return;
        var ph = document.createElement('option');
        ph.value = '';
        ph.textContent = idx === 0 ? '主担当' : '副担当なし';
        sel.innerHTML = '';
        sel.appendChild(ph);
        staff.forEach(function (s) {
          var opt = document.createElement('option');
          opt.value = s.user_id || '';
          opt.textContent = s.shokuin_kj || s.user_id || '';
          sel.appendChild(opt);
        });
      });
    }
  }

  // ==========================================================================
  // 画面配線本体（初期データ適用後に実行する）
  // ==========================================================================
  function initWiring() {

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

    // AI要約（ローカル簡易処理：要約APIは対象外のため現行動作を維持）
    function aiSummarize(text) {
      const t = (text || '').trim();
      if (!t) return '';
      const sentences = t.split('。').map(s => s.trim()).filter(Boolean);
      return sentences.slice(0, 2).join('。') + (sentences.length ? '。' : '');
    }

    const contentEl = document.getElementById('mi-content');

    const csrfTokenEl = document.querySelector('input[name="csrf_token"]');
    const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

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

    // ------------------------------------------------------------------
    // 内容整形ボタン（AIFORMATAPI）：内容欄の文章をサーバー側で整形する
    // ------------------------------------------------------------------
    const contentFormatBtn = document.getElementById('mi-content-ai-format');
    if (contentFormatBtn && contentEl) {
      contentFormatBtn.addEventListener('click', () => {
        if (!contentEl.value.trim()) {
          Toast.error('内容が未入力のため整形できません');
          return;
        }
        callApi('./aiformatapi.do', { transcript: contentEl.value }).then((data) => {
          if (data.e) { Toast.error(data.e); return; }
          contentEl.value = data.dragTranscript || contentEl.value;
          Toast.success('内容の誤字脱字等をAIで整形しました');
        }).catch(() => Toast.error('通信エラーが発生しました'));
      });
    }

    // ------------------------------------------------------------------
    // 帳票出力ボタン（FORMEXPORTAPI）：v_output_reports_csvからExcel出力する
    // ------------------------------------------------------------------
    const exportBtn = document.getElementById('mi-form-export-btn');
    const formSelect = document.getElementById('mi-form');
    if (exportBtn && formSelect) {
      exportBtn.addEventListener('click', () => {
        if (!formSelect.value) {
          Toast.error('帳票を選択してください');
          return;
        }
        // FORMEXPORTAPIはExcelファイルをダウンロードする（JSONではないためfetchで直接取得）
        fetch('./formexportapi.do', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ formcode: formSelect.value, reportid: state.lastDraftReportId || '', source: (function(){ var f = document.getElementById('mi-entry-form'); return f ? (f.getAttribute('data-screen') || '') : ''; })() }),
        }).then((response) => {
          var ct = response.headers.get('content-type') || '';
          if (ct.indexOf('application/vnd.openxmlformats') >= 0 || ct.indexOf('application/octet-stream') >= 0) {
            // Excel ファイルダウンロード
            return response.blob().then((blob) => {
              var url = URL.createObjectURL(blob);
              var a = document.createElement('a');
              a.href = url;
              var disposition = response.headers.get('Content-Disposition') || '';
              // filename*=UTF-8''エンコード形式を優先的に解析する（日文ファイル名対応）
              var mStar = disposition.match(/filename\*=UTF-8''([^;]+)/i);
              var m = disposition.match(/filename=([^;]+)/i);
              var fileName = '';
              if (mStar && mStar[1]) {
                try { fileName = decodeURIComponent(mStar[1].replace(/["']/g, '')); } catch (e) { fileName = mStar[1].replace(/["']/g, ''); }
              } else if (m && m[1]) {
                try { fileName = decodeURIComponent(m[1].replace(/["']/g, '')); } catch (e) { fileName = m[1].replace(/["']/g, ''); }
              }
              a.download = fileName || ('Report_' + (formSelect.value || '') + '.xlsx');
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              URL.revokeObjectURL(url);
              Toast.success('帳票をExcel出力しました');
            });
          }
          // JSON エラーレスポンス
          return response.text().then((text) => {
            var data = null;
            try { data = text ? JSON.parse(text) : {}; } catch (e) { data = { e: text }; }
            Toast.error((data && data.e) || '帳票出力に失敗しました');
          });
        }).catch(() => Toast.error('通信エラーが発生しました'));
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

    // ------------------------------------------------------------------
    // 下書き保存（DRAFTSAVEAPI）：報告書項目一式をDBへ保存する（status='下書き'）
    // ------------------------------------------------------------------
    function saveDraft() {
      if (!contentEl || !contentEl.value.trim()) {
        Toast.error('内容が未入力のため下書き保存できません');
        return;
      }
      const themeCodes = [...document.querySelectorAll('.mi-theme-checkbox')]
        .filter((c) => c.checked).map((c) => c.value);
      const body = {
        houkokushokoumokuisshiki: {
          formcode: formSelect ? formSelect.value : '',
          reportdate: val('mi-date'),
          timestart: val('mi-time-start'),
          timeend: val('mi-time-end'),
          businessname: val('mi-jigyosho'),
          industrycode: val('mi-industry'),
          staffmainname: selectedText('mi-staff-main'),
          staffsubname: selectedText('mi-staff-sub'),
          content: contentEl.value,
          summary: overviewEl ? overviewEl.value : '',
          voicetranscript: val('mi-transcript-display'),
          themecodes: themeCodes,
          reportid: state.lastDraftReportId,
        },
      };
      // ファイル選択がある場合はmultipartで添付ファイルを一緒に送信する
      const attachFiles = getSelectedAttachments();
      let saveRequest;
      if (attachFiles.length) {
        const fd = new FormData();
        fd.append('houkokushokoumokuisshiki', JSON.stringify(body.houkokushokoumokuisshiki));
        attachFiles.forEach((f) => fd.append('attachments', f));
        saveRequest = callApiMultipart('./draftsaveapi.do', fd);
      } else {
        saveRequest = callApi('./draftsaveapi.do', body);
      }
      saveRequest.then((data) => {
        if (data.e) { Toast.error(data.e); return; }
        if (data.dragReportId) state.lastDraftReportId = data.dragReportId;
        clearSelectedAttachments();
        Toast.success(data.i || '下書きとして保存しました');
      }).catch(() => Toast.error('通信エラーが発生しました'));
    }

    {
      const miForm = document.querySelector('#mi-submit')?.form;
      if (miForm) {
        miForm.addEventListener('submit', (e) => {
          const isDraft = e.submitter && e.submitter.value === 'draft';

          if (isDraft) {
            e.preventDefault();
            // 下書き保存はDRAFTSAVEAPI（実データ登録）へ接続
            saveDraft();
            return;
          }
          if (!isDraft) {
            e.preventDefault();
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
            const currentThemeCheckboxes = document.querySelectorAll('.mi-theme-checkbox');
            if (currentThemeCheckboxes.length) {
              const hasTheme = [...currentThemeCheckboxes].some((c) => c.checked);
              setThemeInvalid(!hasTheme);
              if (!hasTheme) missingLabels.push('支援テーマ');
            }
            if (missingLabels.length) {
              Toast.error(`必須項目（※）が未入力です。ご確認ください（未入力: ${missingLabels.join('、')}）`);
              const firstInvalid = document.querySelector('.is-invalid');
              if (firstInvalid) firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
              return;
            }
            // 登録する：FORMNEWSAVEAPI（実データ登録）へ接続
            const checkedThemes = [...document.querySelectorAll('.mi-theme-checkbox:checked')].map((c) => c.value).join(',');
            var elById = function(id) { var el = document.getElementById(id); return el ? el.value : ''; };
            const payload = {
              formcode: elById('mi-form'),
              reportdate: elById('mi-date'),
              timestart: elById('mi-time-start'),
              timeend: elById('mi-time-end'),
              staffmaincode: elById('mi-staff-main'),
              staffsubcode: elById('mi-staff-sub'),
              themecodes: checkedThemes,
              industry: elById('mi-industry'),
              businessname: elById('mi-jigyosho'),
              businessperson: elById('mi-tantosha'),
              content: contentEl ? contentEl.value : '',
              summary: overviewEl ? overviewEl.value : '',
              status: '登録済み',
            };
            var submitSuccess = false;
            // ファイル選択がある場合はmultipartで添付ファイルを一緒に送信する
            const submitAttachFiles = getSelectedAttachments();
            let saveRequest;
            if (submitAttachFiles.length) {
              const fd = new FormData();
              Object.keys(payload).forEach((k) => fd.append(k, payload[k] == null ? '' : payload[k]));
              submitAttachFiles.forEach((f) => fd.append('attachments', f));
              saveRequest = callApiMultipart('./formnewsaveapi.do', fd);
            } else {
              saveRequest = callApi('./formnewsaveapi.do', payload);
            }
            saveRequest.then((data) => {
              if (data.e) { Toast.error(data.e); return; }
              submitSuccess = true;
              state.lastDraftReportId = data.dragReportId || '';
              clearSelectedAttachments();
              Toast.success(data.i || '報告書を登録しました');
            }).catch(() => Toast.error('通信エラーが発生しました')).finally(() => {
              // 失敗時のみsubmitボタンを再び有効化する（成功時は二重登録防止のため無効維持）
              if (!submitSuccess) {
                miForm.querySelectorAll('button[type="submit"]').forEach((btn) => { btn.disabled = false; });
              }
            });
          }
          setTimeout(() => {
            miForm.querySelectorAll('button[type="submit"]').forEach((btn) => { btn.disabled = true; });
          }, 0);
        });
      }
    }

    // ------------------------------------------------------------------
    // 音声パネル（VOICERECORDAPI／VOICEUPLOADAPI／VOICEEXTENDAPI／VOICEINSERTCONTENTAPI）
    // ------------------------------------------------------------------
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

    const transcriptDisplayEl = document.getElementById('mi-transcript-display');

    const applyTranscriptDisplayBtn = document.getElementById('mi-transcript-apply-btn');
    const audioPlayer = document.getElementById('mi-audio-player');
    const maximizeBtn = document.getElementById('mi-voice-maximize');
    const expiryNote = document.getElementById('mi-voice-expiry-note');
    const voiceBtnHint = document.getElementById('mi-voice-btn-hint');

    if (voiceCard) {
      let audioBlobUrl = null;
      let timerTotal = DEFAULT_TIMER_SECONDS;
      let timerRemaining = DEFAULT_TIMER_SECONDS;
      let voiceMaximized = false;

      // 実録音用（MediaRecorder）
      let mediaRecorder = null;
      let mediaChunks = [];
      let mediaStream = null;
      let recordTimerId = null;

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
        if (transcriptDisplayEl) transcriptDisplayEl.disabled = !enabled;
        if (applyTranscriptDisplayBtn) applyTranscriptDisplayBtn.disabled = !enabled;

        if (voiceBtnHint) voiceBtnHint.style.display = enabled ? 'none' : '';
      }

      consentCheckbox.addEventListener('change', () => {
        if (!consentCheckbox.checked) stopRecording('consent-revoked');
        setControlsEnabled(consentCheckbox.checked);
      });

      function setVoiceBtnLabel(text) {
        const labelEl = voiceBtn.querySelector('.mi-voice-btn-square__label');
        if (labelEl) labelEl.textContent = text; else voiceBtn.textContent = text;
      }

      // ----------------------------------------------------------------
      // 録音停止（VOICERECORDAPI action=stop をサーバーへ記録し、
      // 録音データをVOICEUPLOADAPIでサーバー保存する）
      // ----------------------------------------------------------------
      function stopRecording(reason) {
        if (recordTimerId === null) return;
        clearInterval(recordTimerId);
        recordTimerId = null;
        setVoiceBtnLabel('音声入力');
        voiceBtn.classList.remove('is-recording');

        // 録音停止時刻をサーバーへ記録する（VOICERECORDAPI）
        callApi('./voicerecordapi.do', { action: 'stop', reportid: state.lastDraftReportId })
          .catch(() => {});

        // 実録音中の場合はMediaRecorderを停止し、onstopでアップロードする
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
          try { mediaRecorder.stop(); } catch (e) { /* 既に停止済みの場合は無視 */ }
        }
        if (mediaStream) {
          mediaStream.getTracks().forEach((t) => t.stop());
          mediaStream = null;
        }

        if (reason === 'consent-revoked') {
          Toast.error('同意が解除されたため録音を停止しました');
          return;
        }
        if (reason === 'timeout') {
          Toast.success('録音時間の上限に達したため停止し、音声を保存しました');
        } else {
          Toast.success('録音を停止し、音声を保存しました');
        }
      }

      // ----------------------------------------------------------------
      // 録音データのサーバー保存（VOICEUPLOADAPI：multipart実ファイル保存）
      // ----------------------------------------------------------------
      function uploadVoiceBlob(blob, filename) {
        const fd = new FormData();
        fd.append('audio_file', blob, filename);
        fd.append('reportid', state.lastDraftReportId || '');
        fetch('./voiceuploadapi.do', {
          method: 'POST',
          credentials: 'same-origin',
          headers: { 'X-CSRFToken': csrfToken },
          body: fd,
        }).then((r) => r.json()).then((data) => {
          if (data && data.e) { Toast.error(data.e); return; }
          // サーバー算出の削除予定日（30日後）を表示する（実データ）
          if (expiryNote && data.dragDeleteDate) {
            expiryNote.textContent = '音声ファイルの削除予定日: ' + String(data.dragDeleteDate).replace(/-/g, '/')
              + '（録音した日から30日後に自動的に削除されます）';
          }
          // 文字起こし欄を手入力可能にする（録音データはサーバーに保存済み）
          if (transcriptDisplayEl) {
            transcriptDisplayEl.readOnly = false;
            if (!transcriptDisplayEl.value.trim()) {
              transcriptDisplayEl.placeholder = '文字起こし結果を入力できます（AI整形ボタンで整えられます）';
            }
          }
          Toast.success('音声ファイルを保存しました（' + (data.dragFileName || '') + '）');
        }).catch(() => Toast.error('音声ファイルのアップロードに失敗しました'));
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
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          Toast.error('このブラウザでは録音が利用できません');
          return;
        }
        // マイクを取得して実録音を開始する（MediaRecorder）
        navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
          mediaStream = stream;
          mediaChunks = [];
          try {
            mediaRecorder = new MediaRecorder(stream);
          } catch (e) {
            Toast.error('録音の初期化に失敗しました');
            stream.getTracks().forEach((t) => t.stop());
            return;
          }
          mediaRecorder.ondataavailable = (ev) => {
            if (ev.data && ev.data.size) mediaChunks.push(ev.data);
          };
          mediaRecorder.onstop = () => {
            const blob = new Blob(mediaChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
            mediaChunks = [];
            if (blob.size) {
              if (audioBlobUrl) URL.revokeObjectURL(audioBlobUrl);
              audioBlobUrl = URL.createObjectURL(blob);
              playBtn.disabled = !consentCheckbox.checked;
              // 録音データをサーバーへアップロードする（VOICEUPLOADAPI）
              uploadVoiceBlob(blob, 'recording.webm');
            }
          };
          mediaRecorder.start();

          setVoiceBtnLabel('⏹ 停止');
          voiceBtn.classList.add('is-recording');
          // 録音開始時刻をサーバーへ記録する（VOICERECORDAPI）
          callApi('./voicerecordapi.do', { action: 'start', reportid: state.lastDraftReportId })
            .catch(() => {});
          recordTimerId = setInterval(() => {
            timerRemaining--;
            updateTimerDisplay();
            if (timerRemaining <= 0) stopRecording('timeout');
          }, 1000);
        }).catch(() => {
          Toast.error('マイクへのアクセスが許可されなかったため録音を開始できません');
        });
      });

      // ----------------------------------------------------------------
      // 音声ファイルアップロード（VOICEUPLOADAPI：選択ファイルをサーバー保存）
      // ----------------------------------------------------------------
      uploadInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        if (audioBlobUrl) URL.revokeObjectURL(audioBlobUrl);
        audioBlobUrl = URL.createObjectURL(file);
        playBtn.disabled = !consentCheckbox.checked;
        // 選択ファイルをサーバーへアップロードする（VOICEUPLOADAPI：実保存）
        const fd = new FormData();
        fd.append('audio_file', file, file.name);
        fd.append('reportid', state.lastDraftReportId || '');
        fetch('./voiceuploadapi.do', {
          method: 'POST',
          credentials: 'same-origin',
          headers: { 'X-CSRFToken': csrfToken },
          body: fd,
        }).then((r) => r.json()).then((data) => {
          if (data && data.e) { Toast.error(data.e); return; }
          if (expiryNote && data.dragDeleteDate) {
            expiryNote.textContent = '音声ファイルの削除予定日: ' + String(data.dragDeleteDate).replace(/-/g, '/')
              + '（作成・アップロード日から1か月後に自動的に削除されます）';
          }
          if (transcriptDisplayEl) {
            transcriptDisplayEl.readOnly = false;
            if (!transcriptDisplayEl.value.trim()) {
              transcriptDisplayEl.placeholder = '文字起こし結果を入力できます（AI整形ボタンで整えられます）';
            }
          }
          Toast.success('音声ファイルをアップロードしました（' + (data.dragFileName || '') + '）');
        }).catch(() => Toast.error('音声ファイルのアップロードに失敗しました'));
      });

      playBtn.addEventListener('click', () => {
        if (!audioBlobUrl) {
          Toast.error('再生できる音声がありません（録音またはアップロードを行ってください）');
          return;
        }
        audioPlayer.src = audioBlobUrl;
        audioPlayer.style.display = '';
        audioPlayer.play();
      });

      // ----------------------------------------------------------------
      // ＋30分延長（VOICEEXTENDAPI：上限3600秒をサーバー側で判定する）
      // ----------------------------------------------------------------
      extendBtn.addEventListener('click', () => {
        if (timerTotal >= MAX_TIMER_SECONDS) return;
        callApi('./voiceextendapi.do', {
          timeremaining: String(timerRemaining),
          timetotal: String(timerTotal),
        }).then((data) => {
          if (data.e) { Toast.error(data.e); return; }
          timerRemaining = parseInt(data.dragTimerRemaining, 10) || timerRemaining;
          timerTotal = parseInt(data.dragTimerTotal, 10) || timerTotal;
          Toast.success('30分延長しました');
          updateTimerDisplay();
        }).catch(() => Toast.error('通信エラーが発生しました'));
      });

      // ----------------------------------------------------------------
      // 内容に転記する（VOICEINSERTCONTENTAPI：文字起こし内容をサーバー経由で反映）
      // ----------------------------------------------------------------
      if (applyTranscriptDisplayBtn && transcriptDisplayEl && contentEl) {
        applyTranscriptDisplayBtn.addEventListener('click', () => {
          if (!transcriptDisplayEl.value.trim()) {
            Toast.error('文字起こし結果がないため転記できません');
            return;
          }
          callApi('./voiceinsertcontentapi.do', { transcript: transcriptDisplayEl.value }).then((data) => {
            if (data.e) { Toast.error(data.e); return; }
            const text = data.dragTranscript || transcriptDisplayEl.value;
            contentEl.value = contentEl.value.trim()
              ? contentEl.value.replace(/\n*$/, '\n') + text
              : text;
            Toast.success('内容欄に追記しました');
          }).catch(() => Toast.error('通信エラーが発生しました'));
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
  }

  // ==========================================================================
  // 起動：画面初期表示APIで帳票・支援テーマ・担当者を実データ取得してから配線する
  // data-screen属性に応じてAPIを切替する：
  //   ai-input（相談を受ける）→ aiinputinitapi.do
  //   manual-input（報告書を作る）→ formnewinitapi.do
  // API取得に失敗した場合は画面定義（HTML）のまま配線のみ行う
  // ==========================================================================
  var initApiUrl = './aiinputinitapi.do';
  var screenType = '';
  var miEntryForm = document.getElementById('mi-entry-form');
  if (miEntryForm && miEntryForm.getAttribute) {
    screenType = miEntryForm.getAttribute('data-screen') || '';
  }
  if (screenType === 'manual-input') {
    initApiUrl = './formnewinitapi.do';
  }
  callApi(initApiUrl, {}).then((data) => {
    applyInitData(
      parseJson(data.dragForms, []),
      parseJson(data.dragThemes, []),
      parseJson(data.dragStaff, []),
    );
    initWiring();
  }).catch(() => initWiring());
})();
