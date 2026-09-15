(function () {
  const root = document.getElementById('knowledge-root');
  if (!root) return;

  let activeTab = document.body.dataset.knowledgeTab || 'document';
  let inlineMode = null; // view | edit | new
  let inlineIndex = null;

  // 原本文書一覧データ（初期表示時に後端APIから取得する）
  let DOCUMENTS = [];

  // 知識データ一覧（初期表示時に後端APIから取得する）
  let ENTRIES = [];

  // 知識データ編集・新規画面の選択用マスタ一覧（フォーム初期表示APIから取得する）
  let ENTRY_FORM_META = { documentList: [], themeList: [], prefectureList: [] };

  const RAG_SETTING = { embedding_model: 'text-embedding-3-large', vector_db: 'pgvector', chunk_size: 800, chunk_overlap: 100 };
  const LAST_SYNCED = '2026-08-22 09:30';
  const COLLECTIONS = [
    { id: 1, name: 'knowledge_national', vector_count: 1284, synced_date: '2026-08-22', status: '同期済み', status_badge_class: 'badge-status-ok' },
    { id: 2, name: 'knowledge_hokkaido', vector_count: 96, synced_date: '2026-08-22', status: '同期済み', status_badge_class: 'badge-status-ok' },
    { id: 3, name: 'knowledge_hokkaido_pending', vector_count: 0, synced_date: '未同期', status: '未同期', status_badge_class: 'badge-status-pending' },
  ];

  // 後端API呼び出しの共通関数（CSRFトークンをヘッダーに付与する）
  function getCsrfToken() {
    const el = document.querySelector('input[name="csrf_token"]');
    return el ? el.value : '';
  }
  async function callApi(url, row) {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ mode: '1', actflg: '1', triggerid: url.replace('/', '').replace('.do', ''), row: row || {} })
    });
    return await res.json();
  }

  // 原本文書一覧を取得するAPI（KnowledgeInitAPI）
  async function loadDocuments() {
    try {
      const data = await callApi('/knowledgeinitapi.do', {});
      const dragB = data.dragB ? JSON.parse(data.dragB) : [];
      DOCUMENTS = dragB.map(function (row) {
        const status = row.status || '公開中';
        return {
          id: row.knowledge_document_id,
          title: row.title || '',
          prefecture_name: row.prefecture_name || null,
          category: row.category || '',
          format: row.format || '',
          file_size_kb: row.file_size_kb ? Number(row.file_size_kb) : 0,
          linked_count: row.linked_count ? Number(row.linked_count) : 0,
          uploaded_date: row.uploaded_date || '',
          status: status,
          status_badge_class: status === '公開中' ? 'badge-status-ok' : status === '審査中' ? 'badge-status-pending' : 'badge-status-new',
          active_version_number: row.active_version_number,
          file_path: row.file_path || ''
        };
      });
      render();
    } catch (e) {
      console.error('文書一覧の取得に失敗しました', e);
    }
  }

  // 原本文書詳細を取得するAPI（DocumentDetailInitAPI）
  async function loadDocumentDetail(docId) {
    try {
      const data = await callApi('/documentdetailinitapi.do', { knowledgedocumentid: String(docId) });
      const detail = data.documentDetail ? JSON.parse(data.documentDetail) : {};
      const status = detail.status || '公開中';
      return {
        id: detail.knowledge_document_id,
        title: detail.title || '',
        prefecture_name: detail.prefecture_name || null,
        category: detail.category || '',
        format: detail.format || '',
        file_size_kb: detail.file_size_kb ? Number(detail.file_size_kb) : 0,
        linked_count: detail.linked_count ? Number(detail.linked_count) : 0,
        uploaded_date: detail.uploaded_date || '',
        status: status,
        status_badge_class: status === '公開中' ? 'badge-status-ok' : status === '審査中' ? 'badge-status-pending' : 'badge-status-new',
        active_version_number: detail.active_version_number,
        file_path: detail.file_path || ''
      };
    } catch (e) {
      console.error('文書詳細の取得に失敗しました', e);
      return null;
    }
  }

  // 原本文書編集画面の初期値を取得するAPI（DocumentFormInitAPI）
  async function loadDocumentForm(docId) {
    try {
      const data = await callApi('/documentforminitapi.do', { id: String(docId) });
      const detail = data.documentDetail ? JSON.parse(data.documentDetail) : {};
      return {
        id: detail.knowledge_document_id,
        title: detail.title || '',
        prefecture_name: detail.prefecture_name || null,
        prefecture_code: detail.prefecture_code || '',
        category: detail.category || '',
        format: detail.format || ''
      };
    } catch (e) {
      console.error('編集画面初期値の取得に失敗しました', e);
      return null;
    }
  }

  // 原本文書新規登録画面の初期値を取得するAPI（DocumentFormNewInitAPI）
  async function loadNewDocumentForm() {
    try {
      const data = await callApi('/documentformnewinitapi.do', {});
      const detail = data.documentDetail ? JSON.parse(data.documentDetail) : {};
      return {
        id: '',
        title: detail.title || '',
        prefecture_name: detail.prefecture_name || null,
        prefecture_code: detail.prefecture_code || '',
        category: detail.category || '',
        format: detail.format || 'PDF'
      };
    } catch (e) {
      console.error('新規登録画面初期値の取得に失敗しました', e);
      return null;
    }
  }

  // 知識データ一覧を取得するAPI（EntriesInitAPI）
  async function loadEntries() {
    try {
      const data = await callApi('/entriesinitapi.do', {});
      const dragB = data.dragB ? JSON.parse(data.dragB) : [];
      ENTRIES = dragB.map(function (row) {
        const status = row.status || '下書き';
        // テーマバッジは後端からJSON文字列で受け取る場合があるためパースする
        let themeBadges = [];
        try {
          themeBadges = typeof row.theme_badges === 'string' ? JSON.parse(row.theme_badges) : (row.theme_badges || []);
        } catch (e2) { themeBadges = []; }
        return {
          id: row.knowledge_entry_id,
          knowledge_code: row.knowledge_code || '',
          title: row.title || '',
          prefecture_code: row.prefecture_code || '',
          prefecture_name: row.prefecture_name || null,
          theme_badges: themeBadges,
          knowledge_document_id: row.knowledge_document_id || '',
          document_title: row.document_title || '',
          updated_date: row.updated_date || '',
          status: status,
          body: row.content || ''
        };
      });
      render();
    } catch (e) {
      console.error('知識データ一覧の取得に失敗しました', e);
    }
  }

  // 知識データ詳細を取得するAPI（EntryDetailInitAPI）
  async function loadEntryDetail(entryId) {
    try {
      const data = await callApi('/entrydetailinitapi.do', { knowledgeentryid: String(entryId) });
      const detail = data.entryDetail ? JSON.parse(data.entryDetail) : {};
      const status = detail.status || '下書き';
      return {
        id: detail.knowledge_entry_id,
        knowledge_code: detail.knowledge_code || '',
        title: detail.title || '',
        prefecture_code: detail.prefecture_code || '',
        prefecture_name: detail.prefecture_name || null,
        theme_badges: detail.theme_badges || [],
        knowledge_document_id: detail.knowledge_document_id || '',
        document_title: detail.document_title || '',
        updated_date: detail.updated_date || '',
        status: status,
        body: detail.content || ''
      };
    } catch (e) {
      console.error('知識データ詳細の取得に失敗しました', e);
      toastError('知識データ詳細の取得に失敗しました');
      return null;
    }
  }

  // 知識データ編集画面の初期値を取得するAPI（EntryFormInitAPI）
  async function loadEntryForm(entryId) {
    try {
      const data = await callApi('/entryforminitapi.do', { knowledgeentryid: String(entryId) });
      const form = data.entryForm ? JSON.parse(data.entryForm) : {};
      ENTRY_FORM_META = {
        documentList: data.documentList ? JSON.parse(data.documentList) : [],
        themeList: data.themeList ? JSON.parse(data.themeList) : [],
        prefectureList: data.prefectureList ? JSON.parse(data.prefectureList) : []
      };
      return {
        id: form.knowledge_entry_id,
        knowledge_code: form.knowledge_code || '',
        title: form.title || '',
        prefecture_code: form.prefecture_code || '',
        prefecture_name: null,
        theme_badges: [],
        theme_ids: form.theme_ids || [],
        knowledge_document_id: form.knowledge_document_id || '',
        document_title: '',
        updated_date: '',
        status: form.status || '下書き',
        body: form.content || ''
      };
    } catch (e) {
      console.error('編集画面初期値の取得に失敗しました', e);
      toastError('編集画面初期値の取得に失敗しました');
      return null;
    }
  }

  // 知識データ新規登録画面の選択用マスタ一覧を取得するAPI（EntryFormNewInitAPI）
  async function loadNewEntryForm() {
    try {
      const data = await callApi('/entryformnewinitapi.do', {});
      ENTRY_FORM_META = {
        documentList: data.documentList ? JSON.parse(data.documentList) : [],
        themeList: data.themeList ? JSON.parse(data.themeList) : [],
        prefectureList: data.prefectureList ? JSON.parse(data.prefectureList) : []
      };
      return true;
    } catch (e) {
      console.error('新規登録画面初期値の取得に失敗しました', e);
      toastError('新規登録画面初期値の取得に失敗しました');
      return false;
    }
  }

  // 知識データを新規登録するAPI（EntrySaveAPI）
  async function saveEntry(fields) {
    try {
      const data = await callApi('/entrysaveapi.do', {
        title: fields.title,
        knowledgedocumentid: fields.knowledge_document_id || '',
        prefecturecode: fields.prefecture_code || '',
        content: fields.content || '',
        themeids: fields.theme_ids || '',
        status: fields.status || '下書き'
      });
      if (data.msg) toastSuccess(data.msg);
      else toastSuccess('知識データを登録しました');
      return true;
    } catch (e) {
      console.error('知識データの登録に失敗しました', e);
      toastError('知識データの登録に失敗しました');
      return false;
    }
  }

  // 知識データを更新するAPI（EntryUpdateAPI）
  async function updateEntry(entryId, fields) {
    try {
      const data = await callApi('/entryupdateapi.do', {
        knowledgeentryid: String(entryId),
        title: fields.title,
        knowledgedocumentid: fields.knowledge_document_id || '',
        prefecturecode: fields.prefecture_code || '',
        content: fields.content || '',
        themeids: fields.theme_ids || '',
        status: fields.status || '下書き'
      });
      if (data.msg) toastSuccess(data.msg);
      else toastSuccess('知識データを保存しました');
      return true;
    } catch (e) {
      console.error('知識データの更新に失敗しました', e);
      toastError('知識データの更新に失敗しました');
      return false;
    }
  }

  // 原本文書を更新するAPI（DocumentUpdateAPI）
  async function updateDocument(docId, fields) {
    try {
      const data = await callApi('/documentupdateapi.do', {
        knowledgedocumentid: String(docId),
        title: fields.title,
        category: fields.category,
        format: fields.format,
        prefecturecode: fields.prefecture_code || '',
        status: fields.status || ''
      });
      if (data.msg) toastSuccess(data.msg);
      else toastSuccess('文書を保存しました');
      return true;
    } catch (e) {
      console.error('文書の更新に失敗しました', e);
      toastError('文書の更新に失敗しました');
      return false;
    }
  }

  // 原本文書を新規登録するAPI（DocumentSaveAPI）
  async function saveDocument(fields) {
    try {
      const data = await callApi('/documentsaveapi.do', {
        title: fields.title,
        category: fields.category,
        format: fields.format,
        prefecturecode: fields.prefecture_code || '',
        filepath: fields.file_path || '',
        filesizekb: fields.file_size_kb || 0,
        status: fields.status || '審査中'
      });
      if (data.msg) toastSuccess(data.msg);
      else toastSuccess('文書を登録しました');
      return true;
    } catch (e) {
      console.error('文書の登録に失敗しました', e);
      toastError('文書の登録に失敗しました');
      return false;
    }
  }

  // 原本文書の新しい版を登録するAPI（DocumentVersionNewAPI）
  async function uploadNewVersion(docId, fields) {
    try {
      const data = await callApi('/documentversionnewapi.do', {
        knowledgedocumentid: String(docId),
        filepath: fields.file_path || '',
        filesizekb: fields.file_size_kb || 0,
        status: fields.status || '審査中'
      });
      if (data.msg) toastSuccess(data.msg);
      else toastSuccess('新しい版を登録しました');
      return true;
    } catch (e) {
      console.error('版の登録に失敗しました', e);
      toastError('版の登録に失敗しました');
      return false;
    }
  }

  // 原本文書のダウンロードAPI（DocumentVersionDownloadAPI）
  // バックエンドからファイルBlobを受信し、ブラウザでダウンロードする
  async function downloadDocument(docId, versionNumber) {
    try {
      const res = await fetch('/documentversiondownloadapi.do', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ mode: '1', actflg: '1', triggerid: 'documentversiondownloadapi', row: { id: String(docId), version: String(versionNumber) } })
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      // カスタムヘッダーX-Download-Filenameからファイル名を取得する（日本語対応）
      const encodedName = res.headers.get('X-Download-Filename') || '';
      let filename = 'download';
      if (encodedName) {
        filename = decodeURIComponent(encodedName);
      } else {
        const cd = res.headers.get('Content-Disposition') || '';
        const match = cd.match(/filename\*?=(?:UTF-8'')?["']?([^"';\n]+)/);
        if (match) filename = decodeURIComponent(match[1]);
      }
      // Blobを受信してダウンロードリンクを生成する
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toastSuccess('ダウンロードしました');
    } catch (e) {
      console.error('ダウンロードに失敗しました', e);
      toastError('ダウンロードに失敗しました');
    }
  }

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
      html += detailRow('テーマ', (entry.theme_badges || []).map(t => `<span class="badge" style="--badge-color:${t.badge_class}">${escSafe(t.label)}</span>`).join(' ') || '—');
      html += '</div><div>';
      html += detailRow('紐付ファイル', staticVal(entry.document_title));
      html += detailRow('更新日', staticVal(entry.updated_date));
      html += detailRow('ステータス', `<span class="badge ${entry.status === '公開中' ? 'badge-status-ok' : 'badge-status-new'}">${escSafe(entry.status)}</span>`);
      html += detailRow('本文', staticVal(entry.body || ''));
    } else {
      // 編集・新規モード：選択用マスタ一覧（ENTRY_FORM_META）からセレクトボックスを生成する
      const scopeOptions = ['<option value="" ' + (!entry || !entry.prefecture_code ? 'selected' : '') + '>全国共有</option>']
        .concat((ENTRY_FORM_META.prefectureList || []).map(function (p) {
          return `<option value="${escSafe(p.prefecture_code)}" ${entry && entry.prefecture_code === String(p.prefecture_code) ? 'selected' : ''}>${escSafe(p.name)}</option>`;
        })).join('');
      const docOptions = ['<option value="">（紐付なし）</option>']
        .concat((ENTRY_FORM_META.documentList || []).map(function (d) {
          return `<option value="${escSafe(d.knowledge_document_id)}" ${entry && entry.knowledge_document_id === String(d.knowledge_document_id) ? 'selected' : ''}>${escSafe(d.title)}</option>`;
        })).join('');
      const selectedThemeIds = (entry && entry.theme_ids) || (entry ? entry.theme_badges.map(function (t) { return String(t.theme_id); }) : []);
      const themeOptions = (ENTRY_FORM_META.themeList || []).map(function (t) {
        return `<option value="${escSafe(t.theme_id)}" ${selectedThemeIds.indexOf(String(t.theme_id)) >= 0 ? 'selected' : ''}>${escSafe(t.label)}</option>`;
      }).join('');
      html += detailRow('タイトル', `<input type="text" class="form-input" id="kn-entry-title" value="${escSafe(entry ? entry.title : '')}">`);
      html += detailRow('適用範囲', `<select class="form-input" id="kn-entry-scope">${scopeOptions}</select>`);
      html += detailRow('紐付ファイル', `<select class="form-input" id="kn-entry-doc">${docOptions}</select>`);
      html += '</div><div>';
      html += detailRow('テーマ', `<select class="form-input" id="kn-entry-theme" multiple size="5">${themeOptions}</select>`);
      html += detailRow('ステータス', `<select class="form-input" id="kn-entry-status">${['公開中', '下書き'].map(s => `<option ${entry && entry.status === s ? 'selected' : (!entry && s === '下書き' ? 'selected' : '')}>${s}</option>`).join('')}</select>`);
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
          <td>${(e.theme_badges || []).map(t => `<span class="badge" style="--badge-color:${t.badge_class}">${escSafe(t.label)}</span>`).join(' ')}</td>
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
    // 詳細ボタン：後端APIから文書詳細を取得する（DocumentDetailInitAPI）
    root.querySelectorAll('.kn-doc-detail-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const idx = Number(btn.dataset.index);
        const doc = DOCUMENTS[idx];
        loadDocumentDetail(doc.id).then(function (detail) {
          if (detail) {
            DOCUMENTS[idx] = detail;
            openInline('view', idx);
          }
        });
      });
    });
    // ダウンロードボタン：後端APIからファイルパスを取得する（DocumentVersionDownloadAPI）
    root.querySelectorAll('.kn-doc-download-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const doc = DOCUMENTS[Number(btn.dataset.index)];
        downloadDocument(doc.id, doc.active_version_number || 1);
      });
    });
    // ＋文書を追加するボタン：後端APIから新規画面初期値を取得する（DocumentFormNewInitAPI）
    const addBtn = root.querySelector('#kn-doc-add');
    if (addBtn) addBtn.addEventListener('click', (e) => {
      e.preventDefault();
      loadNewDocumentForm().then(function (form) {
        if (form) openInline('new');
      });
    });

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
        // 新規登録：後端APIで文書を登録する（DocumentSaveAPI）
        saveDocument({
          title: title,
          prefecture_code: scope === '北海道' ? '01' : '',
          category: category,
          format: format,
          status: status,
          file_path: '',
          file_size_kb: 0
        }).then(function (ok) {
          if (ok) {
            inlineMode = null;
            inlineIndex = null;
            loadDocuments();
          }
        });
      } else {
        // 編集保存：後端APIで文書を更新する（DocumentUpdateAPI）
        const doc = DOCUMENTS[inlineIndex];
        updateDocument(doc.id, {
          title: title,
          prefecture_code: scope === '北海道' ? '01' : '',
          category: category,
          format: format,
          status: status
        }).then(function (ok) {
          if (ok) {
            Object.assign(doc, { title, prefecture_name: scope || null, category, format, status, status_badge_class: badge });
            inlineMode = 'view';
            render();
          }
        });
      }
    });
  }

  function wireEntryPanel() {
    // 詳細ボタン：後端APIから知識データ詳細を取得する（EntryDetailInitAPI）
    root.querySelectorAll('.kn-entry-detail-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const idx = Number(btn.dataset.index);
        const entry = ENTRIES[idx];
        loadEntryDetail(entry.id).then(function (detail) {
          if (detail) {
            ENTRIES[idx] = detail;
            openInline('view', idx);
          }
        });
      });
    });
    // ＋知識データを登録ボタン：後端APIから新規画面の選択用マスタ一覧を取得する（EntryFormNewInitAPI）
    const addBtn = root.querySelector('#kn-entry-add');
    if (addBtn) addBtn.addEventListener('click', (e) => {
      e.preventDefault();
      loadNewEntryForm().then(function (ok) {
        if (ok) openInline('new');
      });
    });

    const editBtn = root.querySelector('#kn-entry-edit');
    if (editBtn) editBtn.addEventListener('click', () => {
      // 編集モード：後端APIから編集画面初期値を取得する（EntryFormInitAPI）
      const entry = ENTRIES[inlineIndex];
      loadEntryForm(entry.id).then(function (form) {
        if (form) {
          ENTRIES[inlineIndex] = Object.assign({}, ENTRIES[inlineIndex], form);
          inlineMode = 'edit';
          render();
        }
      });
    });
    const closeBtn = root.querySelector('#kn-entry-close');
    if (closeBtn) closeBtn.addEventListener('click', () => {
      if (inlineMode === 'edit') { inlineMode = 'view'; render(); } else { closeInline(); }
    });
    const saveBtn = root.querySelector('#kn-entry-save');
    if (saveBtn) saveBtn.addEventListener('click', () => {
      const title = ((root.querySelector('#kn-entry-title') || {}).value || '').trim();
      if (!title) { toastError('タイトルは必須です'); return; }
      const scope = (root.querySelector('#kn-entry-scope') || {}).value || '';
      const docId = (root.querySelector('#kn-entry-doc') || {}).value || '';
      // テーマは複数選択（select multiple）の選択値をカンマ区切りで送信する
      const themeSelect = root.querySelector('#kn-entry-theme');
      const themeIds = themeSelect ? Array.from(themeSelect.selectedOptions || []).map(function (op) { return op.value; }).filter(function (v) { return v !== ''; }) : [];
      const status = (root.querySelector('#kn-entry-status') || {}).value || '下書き';
      const body = (root.querySelector('#kn-entry-body') || {}).value || '';
      const fields = {
        title: title,
        prefecture_code: scope,
        knowledge_document_id: docId,
        theme_ids: themeIds.join(','),
        status: status,
        content: body
      };
      if (inlineMode === 'new') {
        // 新規登録：後端APIで知識データを登録する（EntrySaveAPI）
        saveEntry(fields).then(function (ok) {
          if (ok) {
            inlineMode = null;
            inlineIndex = null;
            loadEntries();
          }
        });
      } else {
        // 編集保存：後端APIで知識データを更新する（EntryUpdateAPI）
        const entry = ENTRIES[inlineIndex];
        updateEntry(entry.id, fields).then(function (ok) {
          if (ok) {
            inlineMode = null;
            inlineIndex = null;
            loadEntries();
          }
        });
      }
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
      // 知識データタブ表示時に後端APIから最新の一覧を取得する（EntriesInitAPI）
      if (activeTab === 'entry') loadEntries();
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

  // 画面初期表示時に原本文書一覧を取得する（KnowledgeInitAPI）
  window.__renderKnowledge = () => {
    activeTab = 'document';
    inlineMode = null;
    inlineIndex = null;
    loadDocuments();
  };
  loadDocuments();
  // 知識データタブが初期表示の場合は知識データ一覧も取得する（EntriesInitAPI）
  if (activeTab === 'entry') loadEntries();
})();
