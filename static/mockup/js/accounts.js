(function () {
  const root = document.getElementById('accounts-root');
  if (!root) return;

  const QUALIFICATIONS = [
    { code: 'sme_consultant', label: '中小企業診断士' },
    { code: 'labor_consultant', label: '社会保険労務士' },
  ];
  let PERMISSION_LEVELS = ['管理者', '一般職員'];
  let PREFECTURE_OPTIONS = [];
  let SHOKOKAI_OPTIONS = [];
  let ORG_NAME = '—';

  function currentUserAccountId() {
    var raw = (typeof localStorage !== 'undefined' && localStorage.getItem('user_account_id')) || '';
    var n = Number(raw);
    return n > 0 ? n : null;
  }

  // ACCOUNTS: サーバ（ロール可視範囲 + UI絞込）から取得した一覧
  let ACCOUNTS = [];
  let nextAccountId = 1;
  let loadingAccounts = false;

  function getCsrfToken() {
    const el = document.querySelector('input[name="csrf_token"]');
    return el ? el.value : '';
  }

  function currentUiRole() {
    var el = document.getElementById('org-role-select');
    return el ? el.value : 'shokokai';
  }

  function orgFromClient() {
    if (window.ApiClient && typeof window.ApiClient.orgContext === 'function') {
      return window.ApiClient.orgContext() || {};
    }
    var pref = (typeof localStorage !== 'undefined' && localStorage.getItem('prefecture_code')) || '';
    var sho = (typeof localStorage !== 'undefined' && localStorage.getItem('shokokai_cd')) || '';
    return { prefecturecode: pref, shokokaicd: sho };
  }

  function postAccountsApi(url, body) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify(body || {}),
    }).then(function (response) {
      return response.text().then(function (text) {
        var data = null;
        try { data = text ? JSON.parse(text) : {}; } catch (e) { data = { e: text }; }
        // セッション切れ（サーバーが r にスクリプトを返す）
        if (data && data.r && !data.dragB && !data.account && !data.useraccountid && !data.permissionlevels && !data.shokokaioptions) {
          data.e = data.e || 'セッションが切れました。再ログインしてください';
        }
        if (response.status === 403) {
          data = data || {};
          data.e = data.e || data.message || 'CSRFエラーです。ページを再読み込み（Ctrl+F5）してから再ログインしてください';
        }
        return { ok: response.ok, status: response.status, data: data || {} };
      });
    });
  }

  function toastError(msg) {
    try {
      if (typeof Toast !== 'undefined' && Toast.error) Toast.error(msg);
      else window.alert(msg);
    } catch (e) {
      window.alert(msg);
    }
  }

  function toastOk(msg) {
    try {
      if (typeof Toast !== 'undefined' && Toast.success) Toast.success(msg);
      else window.alert(msg);
    } catch (e) {
      window.alert(msg);
    }
  }

  function parseDragB(data) {
    var raw = data && data.dragB;
    if (raw == null || raw === '') return [];
    if (Array.isArray(raw)) return raw;
    if (typeof raw === 'string') {
      try { return JSON.parse(raw); } catch (e) { return []; }
    }
    return [];
  }

  function normalizeAccountRow(r) {
    var quals = r.qualification_codes;
    if (!Array.isArray(quals)) quals = [];
    return {
      user_account_id: Number(r.user_account_id),
      prefecture_code: r.prefecture_code || '',
      shokokai_cd: r.shokokai_cd || '',
      user_id: r.user_id || '',
      shokuin_kj: r.shokuin_kj || '',
      email: r.email || '',
      permission_level: r.permission_level || '',
      status: Number(r.status) === 1 ? 1 : 0,
      core_linked: !!r.core_linked,
      qualification_codes: quals,
      last_login_at: r.last_login_at || null,
      prefecture_name: r.prefecture_name || '',
      shokokai_name: r.shokokai_name || '',
    };
  }

  function buildFilterPayload() {
    var roleEl = root.querySelector('#f-role');
    var statusEl = root.querySelector('#f-status');
    var searchEl = root.querySelector('#f-search');
    var prefEl = root.querySelector('#accounts-f-pref');
    var shokokaiEl = root.querySelector('#accounts-f-shokokai');
    var uiRole = currentUiRole();

    var permissionlevel = '';
    if (roleEl && roleEl.value && roleEl.value !== '全ロール') {
      permissionlevel = roleEl.value;
    }
    var status = '';
    if (statusEl) {
      if (statusEl.value === '1' || statusEl.value === '利用中') status = '1';
      else if (statusEl.value === '0' || statusEl.value === '利用停止') status = '0';
    }

    // 県/商工会は UI 絞込として送る（ロール可視範囲の内側で DB が適用）
    var pref = '';
    var sho = '';
    if (uiRole === 'national') {
      pref = prefEl && prefEl.value ? prefEl.value : '';
      sho = shokokaiEl && shokokaiEl.value ? shokokaiEl.value : '';
    } else if (uiRole === 'pref') {
      sho = shokokaiEl && shokokaiEl.value ? shokokaiEl.value : '';
    }

    return {
      rolecode: uiRole,
      prefecturecode: pref,
      shokokaicd: sho,
      permissionlevel: permissionlevel,
      status: status,
      corelinked: '',
      keyword: searchEl ? searchEl.value.trim() : '',
    };
  }

  function buildInitPayload() {
    return { rolecode: currentUiRole() };
  }

  function applyInitOptions(data) {
    if (!data) return;
    if (Array.isArray(data.permissionlevels) && data.permissionlevels.length) {
      PERMISSION_LEVELS = data.permissionlevels.map(function (x) { return String(x); }).filter(Boolean);
    }
    if (Array.isArray(data.prefectures)) {
      PREFECTURE_OPTIONS = data.prefectures.map(function (p) {
        return {
          code: String(p.prefecture_code || p.code || ''),
          name: String(p.name || p.short_name || p.prefecture_code || ''),
        };
      }).filter(function (p) { return p.code; });
    }
    if (Array.isArray(data.shokokaioptions)) {
      SHOKOKAI_OPTIONS = data.shokokaioptions.map(function (s) {
        return {
          prefecture_code: String(s.prefecture_code || ''),
          shokokai_cd: String(s.shokokai_cd || ''),
          name: String(s.name || s.shokokai_cd || ''),
        };
      }).filter(function (s) { return s.shokokai_cd; });
    }
  }

  function fillRoleSelect(keepValue) {
    var el = root.querySelector('#f-role');
    if (!el) return;
    var cur = keepValue ? el.value : '';
    el.innerHTML = '<option value="">全ロール</option>' + PERMISSION_LEVELS.map(function (n) {
      return '<option value="' + esc(n) + '">' + esc(n) + '</option>';
    }).join('');
    if (cur && Array.prototype.some.call(el.options, function (o) { return o.value === cur; })) el.value = cur;
    if (typeof SelectWidth !== 'undefined') SelectWidth.fit(el);
  }

  function fillPrefSelect(keepValue) {
    var el = root.querySelector('#accounts-f-pref');
    if (!el) return;
    // 全国連の「全都道府県」は空のまま（DB 側で絞らない）
    var cur = keepValue ? el.value : '';
    el.innerHTML = '<option value="">全都道府県</option>' + PREFECTURE_OPTIONS.map(function (p) {
      return '<option value="' + esc(p.code) + '">' + esc(p.name) + '</option>';
    }).join('');
    if (cur && Array.prototype.some.call(el.options, function (o) { return o.value === cur; })) el.value = cur;
    if (typeof SelectWidth !== 'undefined') SelectWidth.fit(el);
  }

  function fillShokokaiSelect(keepValue) {
    var el = root.querySelector('#accounts-f-shokokai');
    if (!el) return;
    var cur = keepValue ? el.value : '';
    var prefEl = root.querySelector('#accounts-f-pref');
    var pref = prefEl ? prefEl.value : '';
    var rows = SHOKOKAI_OPTIONS;
    if (pref) rows = rows.filter(function (s) { return s.prefecture_code === pref; });
    el.innerHTML = '<option value="">全商工会</option>' + rows.map(function (s) {
      return '<option value="' + esc(s.shokokai_cd) + '">' + esc(s.name) + '</option>';
    }).join('');
    if (cur && Array.prototype.some.call(el.options, function (o) { return o.value === cur; })) el.value = cur;
    if (typeof SelectWidth !== 'undefined') SelectWidth.fit(el);
  }

  function syncFilterFieldVisibility() {
    var role = currentUiRole();
    var prefField = root.querySelector('#accounts-f-pref-field');
    var shokokaiField = root.querySelector('#accounts-f-shokokai-field');
    if (prefField) prefField.style.display = role === 'national' ? '' : 'none';
    if (shokokaiField) shokokaiField.style.display = (role === 'national' || role === 'pref') ? '' : 'none';
  }

  function applyAccounts(rows) {
    ACCOUNTS = (rows || []).map(normalizeAccountRow);
    var maxId = 0;
    ACCOUNTS.forEach(function (a) {
      if (a.user_account_id > maxId) maxId = a.user_account_id;
      if ((!ORG_NAME || ORG_NAME === '—') && a.shokokai_name) {
        ORG_NAME = a.shokokai_name;
      }
    });
    nextAccountId = maxId + 1;
  }

  function loadAccountsFromApi(done) {
    if (loadingAccounts) return;
    loadingAccounts = true;
    var tbody = root.querySelector('#accounts-tbody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="8" class="text-muted">読み込み中...</td></tr>';
    }
    postAccountsApi('./accountsfilterapi.do', buildFilterPayload())
      .then(function (result) {
        loadingAccounts = false;
        if (result.data && result.data.e) {
          toastError(String(result.data.e).trim());
          applyAccounts([]);
        } else if (!result.ok) {
          toastError('アカウント一覧の取得に失敗しました');
          applyAccounts([]);
        } else {
          applyAccounts(parseDragB(result.data));
        }
        if (typeof done === 'function') done();
        else renderRows();
      })
      .catch(function () {
        loadingAccounts = false;
        toastError('アカウント一覧の取得に失敗しました');
        applyAccounts([]);
        if (typeof done === 'function') done();
        else renderRows();
      });
  }

  function loadAccountsInit(done) {
    if (loadingAccounts) return;
    loadingAccounts = true;
    var tbody = root.querySelector('#accounts-tbody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="8" class="text-muted">読み込み中...</td></tr>';
    }
    postAccountsApi('./accountsinitapi.do', buildInitPayload())
      .then(function (result) {
        loadingAccounts = false;
        if (result.data && result.data.e) {
          toastError(String(result.data.e).trim());
          applyAccounts([]);
          if (typeof done === 'function') done();
          else renderRows();
          return;
        }
        if (!result.ok) {
          toastError('アカウント一覧の初期表示に失敗しました');
          applyAccounts([]);
          if (typeof done === 'function') done();
          else renderRows();
          return;
        }
        applyInitOptions(result.data);
        fillRoleSelect(true);
        fillPrefSelect(true);
        fillShokokaiSelect(true);
        // 選択肢反映後、現在の UI 絞込条件で DB 再取得
        loadAccountsFromApi(done);
      })
      .catch(function () {
        loadingAccounts = false;
        toastError('アカウント一覧の初期表示に失敗しました');
        applyAccounts([]);
        if (typeof done === 'function') done();
        else renderRows();
      });
  }

  function joinRow(r) {
    return Object.assign({}, r, {
      status_label: r.status === 1 ? '利用中' : '利用停止',
      status_badge: r.status === 1 ? 'badge-status-ok' : 'badge-status-pending',
      core_linked_label: r.core_linked ? 'あり' : 'なし',
      core_linked_badge: r.core_linked ? 'badge-status-pending' : 'badge-status-new',
      last_login_label: r.last_login_at || '未ログイン',
      qualification_labels: QUALIFICATIONS.filter(q => (r.qualification_codes || []).includes(q.code)).map(q => q.label).join('、') || '（未登録）',
    });
  }

  function render() {
    root.innerHTML = `
      <div class="screen-body screen-body--fill">
        <div class="cat-lbl">🔍 条件を入力すると一覧を絞り込みできます</div>

        <div class="card card--fill" id="accounts-filter-card">
          <div class="card-header" id="accounts-filter-header">
            <div class="filter-row">
              <div class="filter-field"><div class="filter-field__label">権限ロール</div>
                <select class="form-input form-input--compact" id="f-role">
                  <option value="">全ロール</option>${PERMISSION_LEVELS.map(n => `<option value="${esc(n)}">${esc(n)}</option>`).join('')}
                </select>
              </div>
              <div class="filter-field"><div class="filter-field__label">ステータス</div>
                <select class="form-input form-input--compact" id="f-status">
                  <option value="">全ステータス</option>
                  <option value="1" selected>利用中</option>
                  <option value="0">利用停止</option>
                </select>
              </div>

              <div class="filter-field" id="accounts-f-pref-field" style="display:none;">
                <div class="filter-field__label">県</div>
                <select class="form-input form-input--compact" id="accounts-f-pref">
                  <option value="">全都道府県</option>
                </select>
              </div>

              <div class="filter-field" id="accounts-f-shokokai-field" style="display:none;">
                <div class="filter-field__label">商工会</div>
                <select class="form-input form-input--compact" id="accounts-f-shokokai">
                  <option value="">全商工会</option>
                </select>
              </div>
              <div class="filter-field"><div class="filter-field__label">キーワード</div>
                <input type="text" class="form-input form-input--compact" id="f-search" placeholder="ユーザID、職員名、メールアドレスで絞り込みができます">
              </div>
            </div>
            <button type="button" class="btn btn-primary btn-sm" id="accounts-new-btn">アカウントを追加する</button>
          </div>
          <div class="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>ユーザID</th><th>職員名</th><th>メールアドレス</th>
                  <th>権限ロール</th><th>基幹連携</th><th>ステータス</th><th>最終ログイン</th><th class="col-action"></th>
                </tr>
              </thead>
              <tbody id="accounts-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>
    `;
    if (typeof SelectWidth !== 'undefined') {
      SelectWidth.fit(root.querySelector('#f-role'));
      SelectWidth.fit(root.querySelector('#f-status'));
      SelectWidth.fit(root.querySelector('#accounts-f-pref'));
      SelectWidth.fit(root.querySelector('#accounts-f-shokokai'));
      SelectWidth.fitPlaceholder(root.querySelector('#f-search'));
    }
    syncFilterFieldVisibility();
    wireFilters();

    if (typeof alignCardBottomToManualInput === 'function') {
      requestAnimationFrame(() => {
        alignCardBottomToManualInput(root.querySelector('.card.card--fill'), true);
      });
    }

    loadAccountsInit(function () {
      renderRows();
    });
  }

  function renderRows() {
    // 絞込はサーバ側（accountsfilterapi / DB）済み
    const filtered = ACCOUNTS.map(joinRow);

    const inlinePanelRow = `<tr class="am-inline-row"><td colspan="8">${buildDetailPanelHtml()}</td></tr>`;

    let rowsHtml = filtered.map(r => `
      <tr>
        <td>${esc(r.user_id)}</td>
        <td>${esc(r.shokuin_kj)}</td>
        <td>${esc(r.email)}</td>
        <td>${esc(r.permission_level)}</td>
        <td><span class="badge ${r.core_linked_badge}">${r.core_linked_label}</span></td>
        <td><span class="badge ${r.status_badge}">${r.status_label}</span></td>
        <td>${esc(r.last_login_label)}</td>
        <td class="col-action"><button type="button" class="btn btn-primary btn-sm accounts-detail-btn" data-id="${r.user_account_id}">詳細</button></td>
      </tr>
      ${inlineMode && inlineMode !== 'new' && inlineAccountId === r.user_account_id ? inlinePanelRow : ''}
    `).join('') || `<tr><td colspan="8" class="text-muted">該当するアカウントがありません</td></tr>`;

    if (inlineMode === 'new') rowsHtml = inlinePanelRow + rowsHtml;

    root.querySelector('#accounts-tbody').innerHTML = rowsHtml;

    root.querySelectorAll('.accounts-detail-btn').forEach(btn => {
      btn.addEventListener('click', () => openInline('view', Number(btn.dataset.id)));
    });
    wireDetailPanel();
  }

  function wireFilters() {
    ['f-role', 'f-status'].forEach(id => {
      const el = root.querySelector('#' + id);
      if (el) el.addEventListener('change', function () {
        loadAccountsFromApi(function () { renderRows(); });
      });
    });
    const prefEl = root.querySelector('#accounts-f-pref');
    if (prefEl) {
      prefEl.addEventListener('change', function () {
        fillShokokaiSelect(false);
        loadAccountsFromApi(function () { renderRows(); });
      });
    }
    const shoEl = root.querySelector('#accounts-f-shokokai');
    if (shoEl) {
      shoEl.addEventListener('change', function () {
        loadAccountsFromApi(function () { renderRows(); });
      });
    }
    const searchEl = root.querySelector('#f-search');
    if (searchEl) searchEl.addEventListener('input', debounce(function () {
      loadAccountsFromApi(function () { renderRows(); });
    }, 250));
    root.querySelector('#accounts-new-btn').addEventListener('click', () => openInline('new'));
  }

  let inlineMode = null;
  let inlineAccountId = null;
  let detailLoading = false;

  function currentAccount() {
    return ACCOUNTS.find(a => a.user_account_id === inlineAccountId) || null;
  }

  function parseAccountPayload(data) {
    if (!data) return null;
    if (data.account) {
      try {
        var obj = typeof data.account === 'string' ? JSON.parse(data.account) : data.account;
        return normalizeAccountRow(obj);
      } catch (e) { /* fall through */ }
    }
    if (data.user_account_id || data.useraccountid) {
      var quals = data.qualification_codes;
      if (typeof quals === 'string') {
        try { quals = JSON.parse(quals); } catch (e2) { quals = []; }
      }
      return normalizeAccountRow(Object.assign({}, data, {
        user_account_id: data.user_account_id || data.useraccountid,
        qualification_codes: quals || [],
        core_linked: data.core_linked === true || data.core_linked === 'true' || data.corelinked === 'true',
      }));
    }
    return null;
  }

  function upsertAccountLocal(row) {
    if (!row || !row.user_account_id) return;
    var idx = ACCOUNTS.findIndex(a => a.user_account_id === row.user_account_id);
    if (idx >= 0) ACCOUNTS[idx] = Object.assign({}, ACCOUNTS[idx], row);
    else ACCOUNTS.push(row);
  }

  function defaultOrgContext() {
    var org = orgFromClient();
    var pref = org.prefecturecode || '';
    var fromList = (pref && ACCOUNTS.find(function (a) { return a.prefecture_code === pref; }))
      || ACCOUNTS[0]
      || null;
    var prefecturecode = pref || (fromList && fromList.prefecture_code) || '';
    var shokokaicd = org.shokokaicd || (fromList && fromList.shokokai_cd) || '';
    if (!prefecturecode) prefecturecode = '00';
    if (!shokokaicd) shokokaicd = '0021';
    return { prefecturecode: prefecturecode, shokokaicd: shokokaicd };
  }

  function openInline(mode, accountId) {
    inlineMode = mode;
    inlineAccountId = accountId || null;
    if (mode === 'view' && accountId) {
      detailLoading = true;
      renderRows();
      postAccountsApi('./accountsdetailapi.do', { useraccountid: String(accountId) })
        .then(function (result) {
          detailLoading = false;
          if (result.data && result.data.e) {
            toastError(String(result.data.e).trim());
            closeInline();
            return;
          }
          var row = parseAccountPayload(result.data);
          if (row) upsertAccountLocal(row);
          renderRows();
        })
        .catch(function () {
          detailLoading = false;
          toastError('詳細の取得に失敗しました');
          closeInline();
        });
      return;
    }
    if (mode === 'edit' && accountId) {
      detailLoading = true;
      renderRows();
      postAccountsApi('./accounteditinitapi.do', { useraccountid: String(accountId) })
        .then(function (result) {
          detailLoading = false;
          if (result.data && result.data.e) {
            toastError(String(result.data.e).trim());
            inlineMode = 'view';
            renderRows();
            return;
          }
          var row = parseAccountPayload(result.data);
          if (row) upsertAccountLocal(row);
          renderRows();
        })
        .catch(function () {
          detailLoading = false;
          toastError('編集データの取得に失敗しました');
          inlineMode = 'view';
          renderRows();
        });
      return;
    }
    renderRows();
  }

  function closeInline() {
    inlineMode = null;
    inlineAccountId = null;
    detailLoading = false;
    renderRows();
  }

  function buildDetailPanelHtml() {
    if (detailLoading && inlineMode !== 'new') {
      return `<div class="am-inline-panel"><div class="text-muted" style="padding:var(--space-5)">読み込み中...</div></div>`;
    }
    const account = currentAccount();
    const viewing = inlineMode === 'view';
    const editable = inlineMode !== 'view';
    const coreLinked = account ? account.core_linked : false;
    const orgName = (account && account.shokokai_name) || ORG_NAME;

    const identityEditable = editable && !coreLinked;

    const panelTitle = inlineMode === 'new' ? '👤 アカウント新規登録' : inlineMode === 'edit' ? '👤 アカウント編集' : '👤 アカウント詳細情報';

    const row = (label, required, valueHtml) => `
      <div class="detail-row">
        <div class="detail-row__label">${esc(label)}${required ? '<span class="detail-row__required">※</span>' : ''}</div>
        <div class="detail-row__value">${valueHtml}</div>
      </div>
    `;

    const staticOrInput = (val, editableNow, inputHtml) => editableNow ? inputHtml : `<span class="detail-row__static">${esc(val || '')}</span>`;

    const warningHtml = (coreLinked && editable)
      ? `<div class="detail-row"><div class="detail-row__value"><span class="text-danger text-sm">基幹連携が「あり」のため、権限ロール・ステータス以外の項目は変更できません。基幹システム側で変更してください。</span></div></div>`
      : '';

    let leftHtml = '';
    leftHtml += row('商工会', false, `<span class="detail-row__static">${esc(orgName)}</span>`);
    leftHtml += row('ユーザID', true, staticOrInput(account && account.user_id, identityEditable, `<input type="text" class="form-input" id="am-user-id" placeholder="ユーザID" style="max-width:133px" value="${esc(account ? account.user_id : '')}">`));
    leftHtml += row('職員名', true, staticOrInput(account && account.shokuin_kj, identityEditable, `<input type="text" class="form-input" id="am-shokuin-kj" placeholder="職員名" style="max-width:200px" value="${esc(account ? account.shokuin_kj : '')}">`));
    leftHtml += row('メールアドレス', true, staticOrInput(account && account.email, identityEditable, `<input type="text" class="form-input" id="am-email" placeholder="example@example.com" value="${esc(account ? account.email : '')}">`));

    if (coreLinked) {
      leftHtml += row('パスワード', false, `<span class="text-muted text-sm">パスワードは基幹システムで変更してください</span>`);
    } else if (viewing) {
      leftHtml += row('パスワード', false, `<span class="detail-row__static">••••••••</span>`);
    } else {
      leftHtml += row('パスワード', inlineMode === 'new', `<input type="password" class="form-input" id="am-password" placeholder="パスワード" style="max-width:200px">${inlineMode === 'edit' ? '<div class="text-muted text-sm">空欄のままにすると変更されません</div>' : ''}`);
    }

    let rightHtml = '';
    if (viewing) {
      rightHtml += row('権限ロール', false, `<span class="detail-row__static">${esc(account ? account.permission_level : '')}</span>`);
    } else {
      rightHtml += row('権限ロール', false, `<select class="form-input" id="am-permission" style="max-width:200px">${PERMISSION_LEVELS.map(p => `<option value="${esc(p)}" ${account && account.permission_level === p ? 'selected' : (!account && p === '一般職員' ? 'selected' : '')}>${esc(p)}</option>`).join('')}</select>`);
    }

    const selectedQuals = account ? account.qualification_codes : [];
    if (editable && !coreLinked) {
      rightHtml += row('資格<br>（複数選択可）', false, `<div class="checkbox-grid">${QUALIFICATIONS.map(q => `<label><input type="checkbox" class="am-qualification" value="${esc(q.code)}" ${selectedQuals.includes(q.code) ? 'checked' : ''}> ${esc(q.label)}</label>`).join('')}</div>`);
    } else {
      rightHtml += row('資格<br>（複数選択可）', false, `<span class="detail-row__static">${esc(QUALIFICATIONS.filter(q => selectedQuals.includes(q.code)).map(q => q.label).join('、') || '（未登録）')}</span>`);
    }

    rightHtml += row('基幹連携', false, `<span class="badge ${coreLinked ? 'badge-status-pending' : 'badge-status-new'}">${coreLinked ? 'あり' : 'なし'}</span>`);

    if (viewing) {
      rightHtml += row('ステータス', false, `<span class="badge ${account && account.status === 1 ? 'badge-status-ok' : 'badge-status-pending'}">${account && account.status === 1 ? '利用中' : '利用停止'}</span>`);
    } else {
      rightHtml += row('ステータス', false, `<select class="form-input" id="am-status" style="max-width:133px"><option value="1" ${!account || account.status === 1 ? 'selected' : ''}>利用中</option><option value="0" ${account && account.status === 0 ? 'selected' : ''}>利用停止</option></select>`);
    }

    if (inlineMode !== 'new') {
      rightHtml += row('最終ログイン日時', false, `<span class="detail-row__static">${esc((account && account.last_login_at) || '未ログイン')}</span>`);
    }

    const html = warningHtml + `<div class="grid grid-2 grid-gap-lg">
      <div>${leftHtml}</div>
      <div>${rightHtml}</div>
    </div>`;

    const actions = viewing
      ? `<div class="flex items-center gap-sm" style="justify-content:flex-end;margin-top:var(--space-6)">
          <button type="button" class="btn btn-primary btn-sm" id="am-edit">編集する</button>
          <button type="button" class="btn btn-outline btn-sm" id="am-close">閉じる</button>
          ${account && currentUserAccountId() && Number(account.user_account_id) !== currentUserAccountId() ? `<button type="button" class="btn btn-danger btn-sm" id="am-delete" style="margin-left:var(--space-8);">削除</button>` : ''}
        </div>`
      : `<div class="flex items-center gap-sm" style="justify-content:flex-end;margin-top:var(--space-6)">
          <button type="button" class="btn btn-outline btn-sm" id="am-cancel">キャンセル</button>
          <button type="button" class="btn btn-primary btn-sm" id="am-save">${inlineMode === 'new' ? '登録する' : '保存する'}</button>
        </div>`;

    return `<div class="am-inline-panel"><div class="card-title" style="background:var(--gold-bg); border-bottom:1px solid var(--gold-border); padding:var(--space-5) var(--space-7); margin:calc(-1 * var(--space-7)) calc(-1 * var(--space-7)) var(--space-4);">${panelTitle}</div>${html}${actions}</div>`;
  }

  function wireDetailPanel() {
    const viewEditBtn = root.querySelector('#am-edit');
    if (viewEditBtn) viewEditBtn.addEventListener('click', () => openInline('edit', inlineAccountId));
    const closeBtn = root.querySelector('#am-close');
    if (closeBtn) closeBtn.addEventListener('click', closeInline);
    const cancelBtn = root.querySelector('#am-cancel');
    if (cancelBtn) cancelBtn.addEventListener('click', () => {
      if (inlineMode === 'edit') { openInline('view', inlineAccountId); } else { closeInline(); }
    });
    const deleteBtn = root.querySelector('#am-delete');
    if (deleteBtn) deleteBtn.addEventListener('click', () => {
      const account = currentAccount();
      if (!account) return;
      if (currentUserAccountId() && Number(account.user_account_id) === currentUserAccountId()) {
        toastError('自分自身のアカウントは削除できません');
        return;
      }
      if (!confirm(`${account.shokuin_kj}（${account.user_id}）を削除しますか？`)) return;
      postAccountsApi('./accountdeleteapi.do', { useraccountid: String(account.user_account_id) })
        .then(function (result) {
          if (result.data && result.data.e) {
            toastError(String(result.data.e).trim());
            return;
          }
          if (result.data && result.data.i) toastOk(String(result.data.i));
          else toastOk('削除しました');
          closeInline();
          loadAccountsFromApi(function () { renderRows(); });
        })
        .catch(function () { toastError('削除に失敗しました'); });
    });
    const saveBtn = root.querySelector('#am-save');
    if (saveBtn) saveBtn.addEventListener('click', saveAccount);
  }

  function saveAccount() {
    const account = currentAccount();
    const coreLinked = account ? account.core_linked : false;
    const identityEditable = !coreLinked;
    const userIdEl = root.querySelector('#am-user-id');
    const shokuinEl = root.querySelector('#am-shokuin-kj');
    const emailEl = root.querySelector('#am-email');
    const passwordEl = root.querySelector('#am-password');
    const permissionEl = root.querySelector('#am-permission');
    const statusEl = root.querySelector('#am-status');

    const user_id = identityEditable ? (userIdEl ? userIdEl.value.trim() : '') : account.user_id;
    const shokuin_kj = identityEditable ? (shokuinEl ? shokuinEl.value.trim() : '') : account.shokuin_kj;
    const email = identityEditable ? (emailEl ? emailEl.value.trim() : '') : account.email;
    const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    if (!user_id || !shokuin_kj || !email) {
      toastError('ユーザID・職員名・メールアドレスは必須です');
      return;
    }
    if (!emailPattern.test(email)) {
      toastError('メールアドレスの形式が正しくありません');
      return;
    }
    if (inlineMode === 'new' && passwordEl && !passwordEl.value) {
      toastError('パスワードを入力してください');
      return;
    }

    const permission_level = permissionEl ? permissionEl.value : (account ? account.permission_level : '一般職員');
    const status = statusEl ? String(statusEl.value) : String(account ? account.status : 1);
    const password = passwordEl ? passwordEl.value : '';
    const org = defaultOrgContext();
    var quals = [];
    var qualEls = root.querySelectorAll('.am-qualification');
    if (qualEls.length) {
      qualEls.forEach(function (cb) { if (cb.checked) quals.push(cb.value); });
    } else if (account && account.qualification_codes) {
      quals = account.qualification_codes.slice();
    }

    if (inlineMode === 'new') {
      const payload = {
        prefecturecode: org.prefecturecode,
        shokokaicd: org.shokokaicd,
        userid: user_id,
        shokuinkj: shokuin_kj,
        email: email,
        password: password,
        permissionlevel: permission_level,
        status: status,
        qualificationcodes: JSON.stringify(quals),
      };
      if (!payload.prefecturecode) {
        toastError('県コードが取得できません。ログイン時の県を確認してください');
        return;
      }
      postAccountsApi('./accountsaveapi.do', payload)
        .then(function (result) {
          if (result.data && result.data.e) {
            toastError(String(result.data.e).trim());
            return;
          }
          if (result.data && result.data.i) toastOk(String(result.data.i));
          else toastOk('登録しました');
          var newId = Number(result.data.useraccountid || result.data.user_account_id || 0);
          inlineMode = 'view';
          inlineAccountId = newId || null;
          loadAccountsFromApi(function () {
            if (newId) openInline('view', newId);
            else renderRows();
          });
        })
        .catch(function () { toastError('登録に失敗しました'); });
      return;
    }

    const payload = {
      useraccountid: String(account.user_account_id),
      prefecturecode: account.prefecture_code || org.prefecturecode,
      shokokaicd: account.shokokai_cd || org.shokokaicd,
      userid: user_id,
      shokuinkj: shokuin_kj,
      email: email,
      password: password,
      permissionlevel: permission_level,
      status: status,
      qualificationcodes: JSON.stringify(quals),
    };
    postAccountsApi('./accountupdateapi.do', payload)
      .then(function (result) {
        if (result.data && result.data.e) {
          toastError(String(result.data.e).trim());
          return;
        }
        if (result.data && result.data.i) toastOk(String(result.data.i));
        else toastOk('更新しました');
        inlineMode = 'view';
        loadAccountsFromApi(function () {
          openInline('view', account.user_account_id);
        });
      })
      .catch(function () { toastError('更新に失敗しました'); });
  }

  window.__renderAccounts = render;
  // ログイン画面では自動取得しない（accounts ルート表示時のみ）
})();
