(function () {
  const root = document.getElementById('knowledge-root');
  if (!root) return;

  let activeTab = document.body.dataset.knowledgeTab || 'document';
  let inlineMode = null; // view | edit | new
  let inlineIndex = null;

  const DOCUMENTS = [
    { id: 1, title: '業務改善助成金 活用事例集', prefecture_name: null, category: '事例集', format: 'PDF', file_size_kb: 2140, linked_count: 4, uploaded_date: '2026-07-02', status: '公開中', status_badge_class: 'badge-status-ok' },
    { id: 2, title: '省エネ設備導入 補助金活用ガイド', prefecture_name: null, category: 'ガイド', format: 'PDF', file_size_kb: 3380, linked_count: 3, uploaded_date: '2026-06-18', status: '公開中', status_badge_class: 'badge-status-ok' },
    { id: 3, title: '北海道 米国関税影響アンケート結果', prefecture_name: '北海道', category: '調査資料', format: 'Excel', file_size_kb: 512, linked_count: 1, uploaded_date: '2026-08-05', status: '審査中', status_badge_class: 'badge-status-pending' },
    { id: 4, title: 'インボイス制度 対応チェックリスト', prefecture_name: null, category: 'チェックリスト', format: 'Word', file_size_kb: 88, linked_count: 5, uploaded_date: '2026-05-20', status: '公開中', status_badge_class: 'badge-status-ok' },
  ];

  const ENTRIES = [
    { id: 1, knowledge_code: 'K-014', title: '業務改善助成金 活用事例集', prefecture_name: null, theme_badges: [{ label: '賃上げ・最低賃金引上げ', badge_class: '#c0392b' }], document_title: '業務改善助成金 活用事例集', updated_date: '2026-07-03', status: '公開中', body: '業務改善助成金を活用した賃上げ事例をまとめたナレッジです。' },
    { id: 2, knowledge_code: 'K-018', title: '省エネ設備導入 補助金活用ガイド', prefecture_name: null, theme_badges: [{ label: 'エネルギー価格・物価の高騰', badge_class: '#1a6fa8' }], document_title: '省エネ設備導入 補助金活用ガイド', updated_date: '2026-06-19', status: '公開中', body: '省エネ設備導入時の補助金活用手順と注意点です。' },
    { id: 3, knowledge_code: 'K-031', title: '米国関税影響を踏まえた販路多角化事例', prefecture_name: '北海道', theme_badges: [{ label: '米国関税', badge_class: '#7a5230' }], document_title: '北海道 米国関税影響アンケート結果', updated_date: '2026-08-06', status: '未公開', body: '米国関税影響を踏まえた販路多角化のヒアリング結果です。' },
    { id: 4, knowledge_code: 'K-009', title: 'インボイス制度 対応チェックリスト', prefecture_name: null, theme_badges: [{ label: 'インボイス制度', badge_class: '#5b3fa0' }], document_title: 'インボイス制度 対応チェックリスト', updated_date: '2026-05-21', status: '公開中', body: 'インボイス制度対応の確認項目一覧です。' },
  ];

  const RAG_SETTING = { embedding_model: 'text-embedding-3-large', vector_db: 'pgvector', chunk_size: 800, chunk_overlap: 100 };
  const LAST_SYNCED = '2026-08-22 09:30';
  const COLLECTIONS = [
    { id: 1, name: 'knowledge_national', vector_count: 1284, synced_date: '2026-08-22', status: '同期済み', status_badge_class: 'badge-status-ok' },
    { id: 2, name: 'knowledge_hokkaido', vector_count: 96, synced_date: '2026-08-22', status: '同期済み', status_badge_class: 'badge-status-ok' },
    { id: 3, name: 'knowledge_hokkaido_pending', vector_count: 0, synced_date: '未同期', status: '未同期', status_badge_class: 'badge-status-pending' },
  ];

  function toastSuccess(msg) {
    if (typeof Toast !== 'undefined' && Toast.success) Toast.success(msg);
    else alert(msg);
  }

  function toastError(msg) {
    if (typeof Toast !== 'undefined' && Toast.error) Toast.error(msg);
    else alert(msg);
  }

  function escSafe(v) {
    if (typeof esc === 'function') return esc(v);
    return String(v == null ? '' : v)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function closeInline() {
    inlineMode = null;
    inlineIndex = null;
    render();
  }

  function openInline(mode, index) {
    inlineMode = mode;
    inlineIndex = typeof index === 'number' ? index : null;
    render();
  }

  function detailRow(label, valueHtml) {
    return `<div class="detail-row"><div class="detail-row__label">${escSafe(label)}</div><div class="detail-row__value">${valueHtml}</div></div>`;
  }

  function staticVal(v) {
    return `<span class="detail-row__static">${escSafe(v == null || v === '' ? '—' : v)}</span>`;
  }

  function panelActions(viewing, editId, closeId, saveId) {
    if (viewing) {
      return `<div class="flex items-center gap-sm" style="justify-content:flex-end;margin-top:var(--space-6)">
        <button type="button" class="btn btn-primary btn-sm" id="${editId}">編集する</button>
        <button type="button" class="btn btn-outline btn-sm" id="${closeId}">閉じる</button>
      </div>`;
    }
    return `<div class="flex items-center gap-sm" style="justify-content:flex-end;margin-top:var(--space-6)">
      <button type="button" class="btn btn-outline btn-sm" id="${closeId}">キャンセル</button>
      <button type="button" class="btn btn-primary btn-sm" id="${saveId}">${inlineMode === 'new' ? '登録する' : '保存する'}</button>
    </div>`;
  }

  function wrapPanel(title, bodyHtml, actionsHtml) {
    return `<tr class="kn-inline-row"><td colspan="12" style="padding:0;background:var(--surface);">
      <div class="am-inline-panel" style="padding:var(--space-7);border-top:1px solid var(--gold-border);border-bottom:1px solid var(--gold-border);">
        <div class="card-title" style="background:var(--gold-bg); border-bottom:1px solid var(--gold-border); padding:var(--space-5) var(--space-7); margin:calc(-1 * var(--space-7)) calc(-1 * var(--space-7)) var(--space-4);">${title}</div>
        ${bodyHtml}${actionsHtml}
      </div>
    </td></tr>`;
  }

  function documentPanelHtml(doc) {
    const viewing = inlineMode === 'view';
    const title = inlineMode === 'new' ? '📄 文書新規登録' : inlineMode === 'edit' ? '📄 文書編集' : '📄 文書詳細情報';
    let html = '<div class="grid grid-2 grid-gap-lg"><div>';
    if (viewing) {
      html += detailRow('タイトル', staticVal(doc.title));
      html += detailRow('適用範囲', staticVal(doc.prefecture_name || '全国共有'));
      html += detailRow('カテゴリ', staticVal(doc.category));
      html += detailRow('形式', staticVal(doc.format));
      html += '</div><div>';
      html += detailRow('サイズ', staticVal(doc.file_size_kb >= 1024 ? (doc.file_size_kb / 1024).toFixed(1) + ' MB' : doc.file_size_kb + ' KB'));
      html += detailRow('紐付け知識数', staticVal(doc.linked_count + '件'));
      html += detailRow('アップロード日', staticVal(doc.uploaded_date));
      html += detailRow('ステータス', `<span class="badge ${doc.status_badge_class}">${escSafe(doc.status)}</span>`);
    } else {
      html += detailRow('タイトル', `<input type="text" class="form-input" id="kn-doc-title" value="${escSafe(doc ? doc.title : '')}">`);
      html += detailRow('適用範囲', `<select class="form-input" id="kn-doc-scope"><option value="" ${!doc || !doc.prefecture_name ? 'selected' : ''}>全国共有</option><option value="北海道" ${doc && doc.prefecture_name === '北海道' ? 'selected' : ''}>北海道</option></select>`);
      html += detailRow('カテゴリ', `<input type="text" class="form-input" id="kn-doc-category" value="${escSafe(doc ? doc.category : '')}">`);
      html += detailRow('形式', `<select class="form-input" id="kn-doc-format">${['PDF', 'Excel', 'Word'].map(f => `<option ${doc && doc.format === f ? 'selected' : ''}>${f}</option>`).join('')}</select>`);
      html += '</div><div>';
      html += detailRow('ステータス', `<select class="form-input" id="kn-doc-status">${['公開中', '審査中', '非公開'].map(s => `<option ${doc && doc.status === s ? 'selected' : (!doc && s === '審査中' ? 'selected' : '')}>${s}</option>`).join('')}</select>`);
      if (inlineMode === 'new') {
        html += detailRow('ファイル', `<input type="file" class="form-input" id="kn-doc-file">`);
      }
    }
    html += '</div></div>';
    return wrapPanel(title, html, panelActions(viewing, 'kn-doc-edit', 'kn-doc-close', 'kn-doc-save'));
  }

  function entryPanelHtml(entry) {
    const viewing = inlineMode === 'view';
    const title = inlineMode === 'new' ? '📚 知識データ新規登録' : inlineMode === 'edit' ? '📚 知識データ編集' : '📚 知識データ詳細';
    let html = '<div class="grid grid-2 grid-gap-lg"><div>';
    if (viewing) {
      html += detailRow('ナレッジコード', staticVal(entry.knowledge_code));
      html += detailRow('タイトル', staticVal(entry.title));
      html += detailRow('適用範囲', staticVal(entry.prefecture_name || '全国共有'));
      html += detailRow('テーマ', entry.theme_badges.map(t => `<span class="badge" style="--badge-color:${t.badge_class}">${escSafe(t.label)}</span>`).join(' ') || '—');
      html += '</div><div>';
      html += detailRow('紐付ファイル', staticVal(entry.document_title));
      html += detailRow('更新日', staticVal(entry.updated_date));
      html += detailRow('ステータス', `<span class="badge ${entry.status === '公開中' ? 'badge-status-ok' : 'badge-status-new'}">${escSafe(entry.status)}</span>`);
      html += detailRow('本文', staticVal(entry.body || ''));
    } else {
      html += detailRow('タイトル', `<input type="text" class="form-input" id="kn-entry-title" value="${escSafe(entry ? entry.title : '')}">`);
      html += detailRow('適用範囲', `<select class="form-input" id="kn-entry-scope"><option value="" ${!entry || !entry.prefecture_name ? 'selected' : ''}>全国共有</option><option value="北海道" ${entry && entry.prefecture_name === '北海道' ? 'selected' : ''}>北海道</option></select>`);
      html += detailRow('紐付ファイル', `<input type="text" class="form-input" id="kn-entry-doc" value="${escSafe(entry ? entry.document_title : '')}">`);
      html += '</div><div>';
      html += detailRow('テーマ', `<input type="text" class="form-input" id="kn-entry-theme" value="${escSafe(entry && entry.theme_badges[0] ? entry.theme_badges[0].label : '')}" placeholder="支援テーマ">`);
      html += detailRow('ステータス', `<select class="form-input" id="kn-entry-status">${['公開中', '未公開'].map(s => `<option ${entry && entry.status === s ? 'selected' : (!entry && s === '未公開' ? 'selected' : '')}>${s}</option>`).join('')}</select>`);
      html += detailRow('本文', `<textarea class="form-input" id="kn-entry-body" rows="4">${escSafe(entry ? (entry.body || '') : '')}</textarea>`);
    }
    html += '</div></div>';
    return wrapPanel(title, html, panelActions(viewing, 'kn-entry-edit', 'kn-entry-close', 'kn-entry-save'));
  }

  function vectorPanelHtml(col) {
    const viewing = inlineMode === 'view';
    const title = inlineMode === 'new' ? '🔢 ベクトルコレクション新規登録' : inlineMode === 'edit' ? '🔢 ベクトルコレクション編集' : '🔢 ベクトルコレクション詳細';
    let html = '<div class="grid grid-2 grid-gap-lg"><div>';
    if (viewing) {
      html += detailRow('コレクション名', staticVal(col.name));
      html += detailRow('ベクトル数', staticVal(col.vector_count.toLocaleString()));
      html += '</div><div>';
      html += detailRow('同期日', staticVal(col.synced_date));
      html += detailRow('ステータス', `<span class="badge ${col.status_badge_class}">${escSafe(col.status)}</span>`);
    } else {
      html += detailRow('コレクション名', `<input type="text" class="form-input" id="kn-vec-name" value="${escSafe(col ? col.name : '')}">`);
      html += detailRow('ベクトル数', `<input type="number" class="form-input" id="kn-vec-count" value="${col ? col.vector_count : 0}">`);
      html += '</div><div>';
      html += detailRow('ステータス', `<select class="form-input" id="kn-vec-status">${['同期済み', '未同期'].map(s => `<option ${col && col.status === s ? 'selected' : (!col && s === '未同期' ? 'selected' : '')}>${s}</option>`).join('')}</select>`);
    }
    html += '</div></div>';
    return wrapPanel(title, html, panelActions(viewing, 'kn-vec-edit', 'kn-vec-close', 'kn-vec-save'));
  }

  function renderTabs() {
    const steps = [
      { key: 'document', num: 1, label: 'ファイル保管' },
      { key: 'entry', num: 2, label: 'タグ付け・レビュー' },
      { key: 'vector', num: 3, label: 'ベクトル反映' },
    ];
    return `<div class="flow-steps">${steps.map((s, i) => `
      ${i > 0 ? '<div class="flow-step__arrow">→</div>' : ''}
      <a href="#" class="flow-step ${activeTab === s.key ? 'is-active' : ''}" data-tab="${s.key}" role="button">
        <div class="flow-step__num">${s.num}</div>
        <div class="flow-step__label">${s.label}</div>
      </a>
    `).join('')}</div>`;
  }

  function renderDocumentTab() {
    const rows = DOCUMENTS.map((d, idx) => {
      let row = `
        <tr>
          <td>${escSafe(d.title)}</td>
          <td>${d.prefecture_name ? `<span class="badge badge-status-new">${escSafe(d.prefecture_name)}</span>` : '<span class="badge">全国共有</span>'}</td>
          <td>${escSafe(d.category)}</td>
          <td>${escSafe(d.format)}</td>
          <td class="num">${d.file_size_kb >= 1024 ? (d.file_size_kb / 1024).toFixed(1) + ' MB' : d.file_size_kb + ' KB'}</td>
          <td class="num">${d.linked_count}件</td>
          <td>${escSafe(d.uploaded_date)}</td>
          <td><span class="badge ${d.status_badge_class}">${escSafe(d.status)}</span></td>
          <td class="col-action"><div class="flex gap-sm">
            <button type="button" class="btn btn-primary btn-sm kn-doc-detail-btn" data-index="${idx}">詳細</button>
            <button type="button" class="btn btn-outline btn-sm kn-doc-download-btn" data-index="${idx}">⬇ ダウンロード</button>
          </div></td>
        </tr>`;
      if (inlineMode && inlineMode !== 'new' && activeTab === 'document' && inlineIndex === idx) {
        row += documentPanelHtml(d);
      }
      return row;
    }).join('');

    let newPanel = '';
    if (inlineMode === 'new' && activeTab === 'document') {
      newPanel = documentPanelHtml(null);
    }

    return `
      <div class="card card--fill" id="kd-documents-card">
        <div class="card-header" id="kd-documents-header">
          <div class="card-title">原本文書 一覧</div>
          <div class="btn-group"><button type="button" class="btn btn-primary--violet btn-sm" id="kn-doc-add">＋ 文書を追加する</button></div>
        </div>
        <div class="table-scroll">
          <table>
            <thead><tr><th>タイトル</th><th>適用範囲</th><th>カテゴリ</th><th>形式</th><th class="num">サイズ</th><th class="num">紐付け知識数</th><th>アップロード日</th><th>ステータス</th><th class="col-action"></th></tr></thead>
            <tbody>${newPanel}${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function renderEntryTab() {
    const rows = ENTRIES.map((e, idx) => {
      let row = `
        <tr>
          <td>${escSafe(e.knowledge_code)}</td>
          <td>${escSafe(e.title)}</td>
          <td>${e.prefecture_name ? `<span class="badge badge-status-new">${escSafe(e.prefecture_name)}</span>` : '<span class="badge">全国共有</span>'}</td>
          <td>${e.theme_badges.map(t => `<span class="badge" style="--badge-color:${t.badge_class}">${escSafe(t.label)}</span>`).join(' ')}</td>
          <td>${escSafe(e.document_title || '—')}</td>
          <td>${escSafe(e.updated_date)}</td>
          <td><span class="badge ${e.status === '公開中' ? 'badge-status-ok' : 'badge-status-new'}">${escSafe(e.status)}</span></td>
          <td class="col-action"><button type="button" class="btn btn-primary btn-sm kn-entry-detail-btn" data-index="${idx}">詳細</button></td>
        </tr>`;
      if (inlineMode && inlineMode !== 'new' && activeTab === 'entry' && inlineIndex === idx) {
        row += entryPanelHtml(e);
      }
      return row;
    }).join('');

    let newPanel = '';
    if (inlineMode === 'new' && activeTab === 'entry') {
      newPanel = entryPanelHtml(null);
    }

    return `
      <div class="card card--fill">
        <div class="card-header">
          <div class="card-title">知識データ 一覧</div>
          <div class="btn-group"><button type="button" class="btn btn-accent btn-sm" id="kn-entry-add">＋ 知識データを登録</button></div>
        </div>
        <div class="table-scroll">
          <table>
            <thead><tr><th>ナレッジコード</th><th>タイトル</th><th>適用範囲</th><th>テーマ</th><th>紐付ファイル</th><th>更新日</th><th>ステータス</th><th class="col-action"></th></tr></thead>
            <tbody>${newPanel}${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function renderVectorTab() {
    const rows = COLLECTIONS.map((c, idx) => {
      let row = `
        <tr>
          <td>${escSafe(c.name)}</td>
          <td class="num">${c.vector_count.toLocaleString()}</td>
          <td>${escSafe(c.synced_date)}</td>
          <td><span class="badge ${c.status_badge_class}">${escSafe(c.status)}</span></td>
          <td class="col-action"><button type="button" class="btn btn-primary btn-sm kn-vec-detail-btn" data-index="${idx}">詳細</button></td>
        </tr>`;
      if (inlineMode && inlineMode !== 'new' && activeTab === 'vector' && inlineIndex === idx) {
        row += vectorPanelHtml(c);
      }
      return row;
    }).join('');

    let newPanel = '';
    if (inlineMode === 'new' && activeTab === 'vector') {
      newPanel = vectorPanelHtml(null);
    }

    return `
      <div class="card" style="margin-bottom:var(--space-8)">
        <div class="card-header"><div class="card-title">RAG設定</div></div>
        <div class="card-body">
          <div class="grid grid-2 grid-gap-md">
            <div><div class="text-sm text-muted">埋め込みモデル</div><div class="font-bold">${escSafe(RAG_SETTING.embedding_model)}</div></div>
            <div><div class="text-sm text-muted">ベクトルDB</div><div class="font-bold">${escSafe(RAG_SETTING.vector_db)}</div></div>
            <div><div class="text-sm text-muted">チャンクサイズ</div><div class="font-bold">${RAG_SETTING.chunk_size.toLocaleString()}</div></div>
            <div><div class="text-sm text-muted">チャンクオーバーラップ</div><div class="font-bold">${RAG_SETTING.chunk_overlap.toLocaleString()}</div></div>
          </div>
        </div>
      </div>
      <div class="card card--fill">
        <div class="card-header">
          <div class="card-title">ベクトルコレクション（最終同期: ${escSafe(LAST_SYNCED || '未同期')}）</div>
          <div class="btn-group">
            <button type="button" class="btn btn-primary btn-sm" id="kn-vec-resync">再同期</button>
            <button type="button" class="btn btn-accent btn-sm" id="kn-vec-add">＋ コレクションを登録</button>
          </div>
        </div>
        <div class="table-scroll">
          <table>
            <thead><tr><th>コレクション名</th><th class="num">ベクトル数</th><th>同期日</th><th>ステータス</th><th class="col-action"></th></tr></thead>
            <tbody>${newPanel}${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function wireDocumentPanel() {
    root.querySelectorAll('.kn-doc-detail-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openInline('view', Number(btn.dataset.index));
      });
    });
    root.querySelectorAll('.kn-doc-download-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const doc = DOCUMENTS[Number(btn.dataset.index)];
        toastSuccess(`${doc.title} をダウンロードしました（モック）`);
      });
    });
    const addBtn = root.querySelector('#kn-doc-add');
    if (addBtn) addBtn.addEventListener('click', (e) => { e.preventDefault(); openInline('new'); });

    const editBtn = root.querySelector('#kn-doc-edit');
    if (editBtn) editBtn.addEventListener('click', () => { inlineMode = 'edit'; render(); });
    const closeBtn = root.querySelector('#kn-doc-close');
    if (closeBtn) closeBtn.addEventListener('click', () => {
      if (inlineMode === 'edit') { inlineMode = 'view'; render(); } else { closeInline(); }
    });
    const saveBtn = root.querySelector('#kn-doc-save');
    if (saveBtn) saveBtn.addEventListener('click', () => {
      const titleEl = root.querySelector('#kn-doc-title');
      const title = titleEl ? titleEl.value.trim() : '';
      if (!title) { toastError('タイトルは必須です'); return; }
      const scope = (root.querySelector('#kn-doc-scope') || {}).value || '';
      const category = (root.querySelector('#kn-doc-category') || {}).value || '';
      const format = (root.querySelector('#kn-doc-format') || {}).value || 'PDF';
      const status = (root.querySelector('#kn-doc-status') || {}).value || '審査中';
      const badge = status === '公開中' ? 'badge-status-ok' : status === '審査中' ? 'badge-status-pending' : 'badge-status-new';
      if (inlineMode === 'new') {
        DOCUMENTS.unshift({
          id: Date.now(), title, prefecture_name: scope || null, category, format,
          file_size_kb: 0, linked_count: 0, uploaded_date: new Date().toISOString().slice(0, 10),
          status, status_badge_class: badge,
        });
        inlineIndex = 0;
        toastSuccess('文書を登録しました');
      } else {
        const doc = DOCUMENTS[inlineIndex];
        Object.assign(doc, { title, prefecture_name: scope || null, category, format, status, status_badge_class: badge });
        toastSuccess('文書を保存しました');
      }
      inlineMode = 'view';
      render();
    });
  }

  function wireEntryPanel() {
    root.querySelectorAll('.kn-entry-detail-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openInline('view', Number(btn.dataset.index));
      });
    });
    const addBtn = root.querySelector('#kn-entry-add');
    if (addBtn) addBtn.addEventListener('click', (e) => { e.preventDefault(); openInline('new'); });

    const editBtn = root.querySelector('#kn-entry-edit');
    if (editBtn) editBtn.addEventListener('click', () => { inlineMode = 'edit'; render(); });
    const closeBtn = root.querySelector('#kn-entry-close');
    if (closeBtn) closeBtn.addEventListener('click', () => {
      if (inlineMode === 'edit') { inlineMode = 'view'; render(); } else { closeInline(); }
    });
    const saveBtn = root.querySelector('#kn-entry-save');
    if (saveBtn) saveBtn.addEventListener('click', () => {
      const title = ((root.querySelector('#kn-entry-title') || {}).value || '').trim();
      if (!title) { toastError('タイトルは必須です'); return; }
      const scope = (root.querySelector('#kn-entry-scope') || {}).value || '';
      const docTitle = (root.querySelector('#kn-entry-doc') || {}).value || '';
      const theme = ((root.querySelector('#kn-entry-theme') || {}).value || '').trim();
      const status = (root.querySelector('#kn-entry-status') || {}).value || '未公開';
      const body = (root.querySelector('#kn-entry-body') || {}).value || '';
      const theme_badges = theme ? [{ label: theme, badge_class: '#1a6fa8' }] : [];
      if (inlineMode === 'new') {
        ENTRIES.unshift({
          id: Date.now(),
          knowledge_code: 'K-' + String(100 + ENTRIES.length).padStart(3, '0'),
          title, prefecture_name: scope || null, theme_badges,
          document_title: docTitle, updated_date: new Date().toISOString().slice(0, 10),
          status, body,
        });
        inlineIndex = 0;
        toastSuccess('知識データを登録しました');
      } else {
        const entry = ENTRIES[inlineIndex];
        Object.assign(entry, {
          title, prefecture_name: scope || null, theme_badges,
          document_title: docTitle, status, body,
          updated_date: new Date().toISOString().slice(0, 10),
        });
        toastSuccess('知識データを保存しました');
      }
      inlineMode = 'view';
      render();
    });
  }

  function wireVectorPanel() {
    root.querySelectorAll('.kn-vec-detail-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openInline('view', Number(btn.dataset.index));
      });
    });
    const addBtn = root.querySelector('#kn-vec-add');
    if (addBtn) addBtn.addEventListener('click', (e) => { e.preventDefault(); openInline('new'); });
    const resyncBtn = root.querySelector('#kn-vec-resync');
    if (resyncBtn) resyncBtn.addEventListener('click', (e) => {
      e.preventDefault();
      toastSuccess('ベクトルコレクションを再同期しました（モック）');
    });

    const editBtn = root.querySelector('#kn-vec-edit');
    if (editBtn) editBtn.addEventListener('click', () => { inlineMode = 'edit'; render(); });
    const closeBtn = root.querySelector('#kn-vec-close');
    if (closeBtn) closeBtn.addEventListener('click', () => {
      if (inlineMode === 'edit') { inlineMode = 'view'; render(); } else { closeInline(); }
    });
    const saveBtn = root.querySelector('#kn-vec-save');
    if (saveBtn) saveBtn.addEventListener('click', () => {
      const name = ((root.querySelector('#kn-vec-name') || {}).value || '').trim();
      if (!name) { toastError('コレクション名は必須です'); return; }
      const count = Number((root.querySelector('#kn-vec-count') || {}).value || 0);
      const status = (root.querySelector('#kn-vec-status') || {}).value || '未同期';
      const badge = status === '同期済み' ? 'badge-status-ok' : 'badge-status-pending';
      if (inlineMode === 'new') {
        COLLECTIONS.unshift({
          id: Date.now(), name, vector_count: count,
          synced_date: status === '同期済み' ? new Date().toISOString().slice(0, 10) : '未同期',
          status, status_badge_class: badge,
        });
        inlineIndex = 0;
        toastSuccess('コレクションを登録しました');
      } else {
        const col = COLLECTIONS[inlineIndex];
        Object.assign(col, {
          name, vector_count: count, status, status_badge_class: badge,
          synced_date: status === '同期済み' ? (col.synced_date === '未同期' ? new Date().toISOString().slice(0, 10) : col.synced_date) : '未同期',
        });
        toastSuccess('コレクションを保存しました');
      }
      inlineMode = 'view';
      render();
    });
  }

  function wireTabs() {
    const usePageNav = typeof window.MockApp !== 'undefined' && window.MockApp.href;
    root.querySelectorAll('.flow-step[data-tab]').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        if (usePageNav) {
          const route = { document: 'knowledge-documents', entry: 'knowledge-data', vector: 'knowledge-vector' }[el.dataset.tab];
          if (route) {
            window.location.href = window.MockApp.href(route);
            return;
          }
        }
        activeTab = el.dataset.tab;
        inlineMode = null;
        inlineIndex = null;
        render();
      });
    });
  }

  function render() {
    const tabHtml = activeTab === 'document' ? renderDocumentTab() : activeTab === 'entry' ? renderEntryTab() : renderVectorTab();
    root.innerHTML = `
      <div class="screen-body screen-body--fill">
        ${renderTabs()}
        <div style="margin-top:var(--space-6)">${tabHtml}</div>
      </div>
    `;
    wireTabs();
    if (activeTab === 'document') wireDocumentPanel();
    if (activeTab === 'entry') wireEntryPanel();
    if (activeTab === 'vector') wireVectorPanel();

    if (typeof alignCardBottomToManualInput === 'function') {
      requestAnimationFrame(() => {
        alignCardBottomToManualInput(root.querySelector('.card.card--fill'), true);
      });
    }
    if (typeof window.__applyRoleAccentColor === 'function') window.__applyRoleAccentColor();
  }

  window.__renderKnowledge = () => { activeTab = 'document'; inlineMode = null; inlineIndex = null; render(); };
  render();
})();
