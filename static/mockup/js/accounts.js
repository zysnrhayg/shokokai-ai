(function () {
  const root = document.getElementById('accounts-root');
  if (!root) return;

  const QUALIFICATIONS = [
    { code: 'sme_consultant', label: '中小企業診断士' },
    { code: 'labor_consultant', label: '社会保険労務士' },
  ];
  const PERMISSION_LEVELS = ['管理者', '一般職員'];
  const ORG_NAME = '北海道商工会連合会';

  const CURRENT_USER_ACCOUNT_ID = 1;

  let ACCOUNTS = [
    { user_account_id: 1, user_id: '012', shokuin_kj: '小島 直樹', email: 'kojima@hokkaido-shokoren.example.jp', permission_level: '管理者', status: 1, core_linked: true, qualification_codes: ['sme_consultant'], last_login_at: '2026/08/22 09:12:03' },
    { user_account_id: 2, user_id: '011', shokuin_kj: '北海道一般', email: 'ippan@hokkaido-shokoren.example.jp', permission_level: '一般職員', status: 1, core_linked: false, qualification_codes: [], last_login_at: '2026/08/20 17:40:11' },
    { user_account_id: 3, user_id: '013', shokuin_kj: '佐藤 恵子', email: 'sato@hokkaido-shokoren.example.jp', permission_level: '一般職員', status: 0, core_linked: false, qualification_codes: ['labor_consultant'], last_login_at: null },
  ];
  let nextAccountId = 4;

  function joinRow(r) {
    return Object.assign({}, r, {
      status_label: r.status === 1 ? '利用中' : '利用停止',
      status_badge: r.status === 1 ? 'badge-status-ok' : 'badge-status-pending',
      core_linked_label: r.core_linked ? 'あり' : 'なし',
      core_linked_badge: r.core_linked ? 'badge-status-pending' : 'badge-status-new',
      last_login_label: r.last_login_at || '未ログイン',
      qualification_labels: QUALIFICATIONS.filter(q => r.qualification_codes.includes(q.code)).map(q => q.label).join('、') || '（未登録）',
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
                  <option>全ロール</option>${PERMISSION_LEVELS.map(n => `<option>${esc(n)}</option>`).join('')}
                </select>
              </div>
              <div class="filter-field"><div class="filter-field__label">ステータス</div>
                <select class="form-input form-input--compact" id="f-status">
                  <option>全ステータス</option><option selected>利用中</option><option>利用停止</option>
                </select>
              </div>

              <div class="filter-field" id="accounts-f-pref-field" style="display:none;">
                <div class="filter-field__label">県</div>
                <select class="form-input form-input--compact" id="accounts-f-pref">
                  <option value="">全都道府県</option>
                  <option>北海道</option><option>青森県</option><option>岩手県</option>
                  <option>宮城県</option><option>秋田県</option><option>山形県</option>
                  <option>福島県</option><option>茨城県</option><option>栃木県</option>
                  <option>群馬県</option><option>埼玉県</option><option>千葉県</option>
                  <option>東京都</option><option>神奈川県</option><option>新潟県</option>
                  <option>富山県</option><option>石川県</option><option>福井県</option>
                  <option>山梨県</option><option>長野県</option><option>岐阜県</option>
                  <option>静岡県</option><option>愛知県</option><option>三重県</option>
                  <option>滋賀県</option><option>京都府</option><option>大阪府</option>
                  <option>兵庫県</option><option>奈良県</option><option>和歌山県</option>
                  <option>鳥取県</option><option>島根県</option><option>岡山県</option>
                  <option>広島県</option><option>山口県</option><option>徳島県</option>
                  <option>香川県</option><option>愛媛県</option><option>高知県</option>
                  <option>福岡県</option><option>佐賀県</option><option>長崎県</option>
                  <option>熊本県</option><option>大分県</option><option>宮崎県</option>
                  <option>鹿児島県</option><option>沖縄県</option>
                </select>
              </div>

              <div class="filter-field" id="accounts-f-shokokai-field" style="display:none;">
                <div class="filter-field__label">商工会</div>
                <select class="form-input form-input--compact" id="accounts-f-shokokai">
                  <option value="">全商工会</option>
                  <option>札幌商工会連合会</option>
                  <option>函館商工会連合会</option>
                  <option>旭川商工会連合会</option>
                  <option>苫小牧商工会連合会</option>
                  <option>釧路商工会連合会</option>
                  <option>帯広商工会連合会</option>
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
    wireFilters();
    renderRows();

    {
      const roleSelect = document.getElementById('org-role-select');
      const shokokaiField = root.querySelector('#accounts-f-shokokai-field');
      if (roleSelect && shokokaiField) {
        const isFederation = roleSelect.value === 'national' || roleSelect.value === 'pref';
        shokokaiField.style.display = isFederation ? '' : 'none';
      }
    }

    if (typeof alignCardBottomToManualInput === 'function') {
      requestAnimationFrame(() => {
        alignCardBottomToManualInput(root.querySelector('.card.card--fill'), true);
      });
    }
  }

  function renderRows() {
    const roleEl = root.querySelector('#f-role');
    const statusEl = root.querySelector('#f-status');
    const searchEl = root.querySelector('#f-search');
    const roleVal = roleEl && roleEl.value !== '全ロール' ? roleEl.value : null;
    const statusVal = statusEl && statusEl.value !== '全ステータス' ? statusEl.value : null;
    const searchVal = searchEl ? searchEl.value.trim().toLowerCase() : '';

    const filtered = ACCOUNTS.map(joinRow).filter(r =>
      (!roleVal || r.permission_level === roleVal) &&
      (!statusVal || r.status_label === statusVal) &&
      (!searchVal || r.shokuin_kj.toLowerCase().includes(searchVal) || r.email.toLowerCase().includes(searchVal) || r.user_id.toLowerCase().includes(searchVal))
    );

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
      if (el) el.addEventListener('change', renderRows);
    });
    const searchEl = root.querySelector('#f-search');
    if (searchEl) searchEl.addEventListener('input', debounce(renderRows, 150));
    root.querySelector('#accounts-new-btn').addEventListener('click', () => openInline('new'));
  }

  let inlineMode = null;
  let inlineAccountId = null;

  function currentAccount() {
    return ACCOUNTS.find(a => a.user_account_id === inlineAccountId) || null;
  }

  function openInline(mode, accountId) {
    inlineMode = mode;
    inlineAccountId = accountId || null;
    renderRows();
  }

  function closeInline() {
    inlineMode = null;
    inlineAccountId = null;
    renderRows();
  }

  function buildDetailPanelHtml() {
    const account = currentAccount();
    const viewing = inlineMode === 'view';
    const editable = inlineMode !== 'view';
    const coreLinked = account ? account.core_linked : false;

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
    leftHtml += row('商工会', false, `<span class="detail-row__static">${esc(ORG_NAME)}</span>`);
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
      rightHtml += row('権限ロール', false, `<span class="detail-row__static">${esc(account.permission_level)}</span>`);
    } else {
      rightHtml += row('権限ロール', false, `<select class="form-input" id="am-permission" style="max-width:200px">${PERMISSION_LEVELS.map(p => `<option ${account && account.permission_level === p ? 'selected' : (!account && p === '一般職員' ? 'selected' : '')}>${esc(p)}</option>`).join('')}</select>`);
    }

    const selectedQuals = account ? account.qualification_codes : [];
    if (editable && !coreLinked) {
      rightHtml += row('資格<br>（複数選択可）', false, `<div class="checkbox-grid">${QUALIFICATIONS.map(q => `<label><input type="checkbox" class="am-qualification" value="${esc(q.code)}" ${selectedQuals.includes(q.code) ? 'checked' : ''}> ${esc(q.label)}</label>`).join('')}</div>`);
    } else {
      rightHtml += row('資格<br>（複数選択可）', false, `<span class="detail-row__static">${esc(QUALIFICATIONS.filter(q => selectedQuals.includes(q.code)).map(q => q.label).join('、') || '（未登録）')}</span>`);
    }

    rightHtml += row('基幹連携', false, `<span class="badge ${coreLinked ? 'badge-status-pending' : 'badge-status-new'}">${coreLinked ? 'あり' : 'なし'}</span>`);

    if (viewing) {
      rightHtml += row('ステータス', false, `<span class="badge ${account.status === 1 ? 'badge-status-ok' : 'badge-status-pending'}">${account.status === 1 ? '利用中' : '利用停止'}</span>`);
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
          ${account.user_account_id !== CURRENT_USER_ACCOUNT_ID ? `<button type="button" class="btn btn-danger btn-sm" id="am-delete" style="margin-left:var(--space-8);">削除</button>` : ''}
        </div>`
      : `<div class="flex items-center gap-sm" style="justify-content:flex-end;margin-top:var(--space-6)">
          <button type="button" class="btn btn-outline btn-sm" id="am-cancel">キャンセル</button>
          <button type="button" class="btn btn-primary btn-sm" id="am-save">${inlineMode === 'new' ? '登録する' : '保存する'}</button>
        </div>`;

    return `<div class="am-inline-panel"><div class="card-title" style="background:var(--gold-bg); border-bottom:1px solid var(--gold-border); padding:var(--space-5) var(--space-7); margin:calc(-1 * var(--space-7)) calc(-1 * var(--space-7)) var(--space-4);">${panelTitle}</div>${html}${actions}</div>`;
  }

  function wireDetailPanel() {
    const viewEditBtn = root.querySelector('#am-edit');
    if (viewEditBtn) viewEditBtn.addEventListener('click', () => { inlineMode = 'edit'; renderRows(); });
    const closeBtn = root.querySelector('#am-close');
    if (closeBtn) closeBtn.addEventListener('click', closeInline);
    const cancelBtn = root.querySelector('#am-cancel');
    if (cancelBtn) cancelBtn.addEventListener('click', () => {
      if (inlineMode === 'edit') { inlineMode = 'view'; renderRows(); } else { closeInline(); }
    });
    const deleteBtn = root.querySelector('#am-delete');
    if (deleteBtn) deleteBtn.addEventListener('click', () => {
      const account = currentAccount();
      if (!account) return;
      if (!confirm(`${account.shokuin_kj}（${account.user_id}）を削除しますか？`)) return;
      ACCOUNTS = ACCOUNTS.filter(a => a.user_account_id !== account.user_account_id);
      Toast.success('削除しました');
      closeInline();
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
    const qualificationCodes = Array.from(root.querySelectorAll('.am-qualification:checked')).map(cb => cb.value);

    const user_id = identityEditable ? (userIdEl ? userIdEl.value.trim() : '') : account.user_id;
    const shokuin_kj = identityEditable ? (shokuinEl ? shokuinEl.value.trim() : '') : account.shokuin_kj;
    const email = identityEditable ? (emailEl ? emailEl.value.trim() : '') : account.email;
    const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    if (!user_id || !shokuin_kj || !email) {
      Toast.error('ユーザID・職員名・メールアドレスは必須です');
      return;
    }
    if (!emailPattern.test(email)) {
      Toast.error('メールアドレスの形式が正しくありません');
      return;
    }
    if (inlineMode === 'new' && passwordEl && !passwordEl.value) {
      Toast.error('パスワードを入力してください');
      return;
    }
    const duplicate = ACCOUNTS.some(a => a.user_id === user_id && (!account || a.user_account_id !== account.user_account_id));
    if (duplicate) {
      Toast.error('同じ県内に同じユーザIDのアカウントが既に存在します');
      return;
    }

    const permission_level = permissionEl ? permissionEl.value : (account ? account.permission_level : '一般職員');
    const status = statusEl ? Number(statusEl.value) : (account ? account.status : 1);

    if (inlineMode === 'new') {
      const newAccount = {
        user_account_id: nextAccountId++, user_id, shokuin_kj, email, permission_level, status,
        core_linked: false, qualification_codes: qualificationCodes, last_login_at: null,
      };
      ACCOUNTS.push(newAccount);
      Toast.success('登録しました');
      inlineAccountId = newAccount.user_account_id;
    } else {
      Object.assign(account, {
        user_id, shokuin_kj, email, permission_level, status,
        qualification_codes: identityEditable ? qualificationCodes : account.qualification_codes,
      });
      Toast.success('登録しました');
    }
    inlineMode = 'view';
    renderRows();
  }

  window.__renderAccounts = render;
  render();
})();
