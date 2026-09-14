(function () {
  const root = document.getElementById('knowledge-search-root');
  if (!root) return;

  const KNOWLEDGE_ENTRIES = [
    { code: 'K-014', title: '業務改善助成金 活用事例集', theme_label: '賃上げ・最低賃金引上げ', badge_color: '#c0392b',
      content: '業務改善助成金を活用して設備投資を行った事例をまとめている。最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できる。対象は事業場内最低賃金と地域別最低賃金の差額が一定以内の中小企業・小規模事業者で、機械設備やPOSシステムなどの導入費用が助成対象になる。申請には賃金引上げ計画と生産性向上計画の提出が必要で、計画作成の段階から相談に乗ることで採択率を高められる。同業種での活用実績も複数あり、具体的な導入機種の選定まで支援できる。',
      ref_info: '同業種が本助成金を活用した際の申請書類の書き方・生産性向上計画の記載例', updated_date: '2026-07-03 10:15' },
    { code: 'K-021', title: '省力化投資による人手不足対応 事例集', theme_label: '省力化促進・人手不足', badge_color: '#2d7a4f',
      content: '省力化補助金を使って設備を導入し、人手不足を解消した中小企業の事例を紹介している。対象はカタログに掲載された汎用性の高い省力化機器（券売機、自動倉庫、清掃ロボット等）で、通常枠より審査から交付までの期間が短いのが特徴。人手不足で業務が回らない事業者ほど効果が出やすく、導入後1年で残業時間が大きく減った例もある。申請はカタログから機種を選ぶだけで比較的容易だが、補助対象外の付帯工事費との切り分けに注意が必要。導入効果の測定方法も併せて案内できる。',
      ref_info: '省力化補助金で設備を導入し人手不足を解消した中小企業の事例', updated_date: '2026-06-05 14:30' },
    { code: 'K-018', title: '省エネ設備導入 補助金活用ガイド', theme_label: 'エネルギー価格・物価の高騰', badge_color: '#1a6fa8',
      content: '空調・照明等の省エネ設備導入で使える補助金の対象要件と申請の流れをまとめたガイド。エネルギー価格高騰で光熱費負担が増している事業者向けに、LED照明や高効率空調への更新費用の一部を補助する制度で、既存設備からの省エネ率が一定以上見込めることが要件になる。申請前にエネルギー診断を受けて削減見込みを算定する必要があり、診断から交付までおおむね数か月かかる点は事前に伝えておきたい。複数年契約の電力調達見直しと組み合わせると効果が大きい。',
      ref_info: '空調・照明等の省エネ設備導入で使える補助金の対象要件と申請の流れ', updated_date: '2026-06-19 09:50' },
    { code: 'K-009', title: 'インボイス制度 対応チェックリスト', theme_label: 'インボイス制度', badge_color: '#5b3fa0',
      content: 'インボイス制度対応で確認すべき請求書様式・経理体制のチェック項目をまとめたリスト。適格請求書発行事業者としての登録有無、請求書への登録番号・税率区分の記載、会計ソフトが電子帳簿保存法の要件も満たしているかを一通り確認できる構成になっている。免税事業者からの仕入れが多い事業者は経過措置の適用期限も要注意で、取引先との価格・契約条件の見直しが必要になる場合がある。チェックリストに沿って進めれば、対応漏れのまま申告時期を迎えるリスクを減らせる。',
      ref_info: 'インボイス制度対応で確認すべき請求書様式・経理体制のチェック項目', updated_date: '2026-05-21 16:05' },
    { code: 'K-031', title: '米国関税影響を踏まえた販路多角化事例', theme_label: '米国関税', badge_color: '#7a5230',
      content: '米国向け輸出に依存していた事業者が販路を多角化した進め方を紹介する事例集。関税率変動の影響をまず数値でシミュレーションし、価格転嫁だけで吸収しきれない部分を東南アジアや国内新規顧客の開拓で補った例をまとめている。展示会出展補助金を使って費用負担を抑えながら新市場を試した事業者や、既存商品を輸出先ごとに仕様変更して展開した事業者の進め方も具体的に紹介する。一国依存からの脱却は時間がかかるため、段階的な計画づくりが重要になる。',
      ref_info: '米国向け輸出に依存していた事業者が販路を多角化した進め方', updated_date: '2026-08-06 11:20' },
    { code: 'K-011', title: '電子帳簿保存法 対応の手引き', theme_label: '電子帳簿保存法', badge_color: '#8a7a3f',
      content: '電子帳簿保存法で求められる保存要件と社内体制整備のポイントを解説した手引き。電子取引データはタイムスタンプや訂正削除履歴が残るシステムでの保存が原則で、紙に印刷しての保存では要件を満たさない点が誤解されやすい。スキャナ保存制度を使えば紙の書類も電子化して保管スペースを削減でき、必要な書類をすぐ検索できるようになる。誰が対応しても同じ運用になるよう、保存規程を整備しておくことが属人化を防ぐ鍵になる。会計システム側のタイムスタンプ対応状況も併せて確認するとよい。',
      ref_info: '電子帳簿保存法で求められる保存要件と社内体制整備のポイント', updated_date: '2026-04-14 13:40' },
    { code: 'K-026', title: '小規模事業者のデジタル化支援まとめ', theme_label: 'デジタル化', badge_color: '#2d6a8f',
      content: '小規模事業者がITツールを導入する際に使える支援策の一覧と選び方をまとめている。会計・受発注業務をクラウド化すれば場所を選ばず業務ができるようになり、キャッシュレス決済の導入は顧客の利便性向上と機会損失の防止につながる。IT導入補助金は対象ツールがあらかじめ登録された制度から選ぶ形式のため、業務の課題を整理してから適したツールを絞り込むのが近道になる。社内にデジタル人材を育てておけば、外部委託に頼らず自走できる体制を作りやすい。',
      ref_info: '小規模事業者がITツールを導入する際に使える支援策の一覧と選び方', updated_date: '2026-07-28 08:55' },
    { code: 'K-005', title: 'コロナ後の販路回復支援事例集', theme_label: '新型コロナ', badge_color: '#6a6a6a',
      content: 'コロナ後の販路回復に向けて新商品開発・新規顧客開拓を行った事例をまとめている。既存の主力商品だけでは客足が戻りきらなかった事業者が、新商品開発や新サービス展開で新しい客層を取り込んだ進め方を紹介する。コロナ融資の返済負担が重い場合は、借換保証制度等で月々の返済額を軽くしながら販路回復に投資する順序が有効だった例もある。事業再構築を伴う新分野展開では、補助金を活用しながら新しい収益の柱を作った事例も収録している。',
      ref_info: 'コロナ後の販路回復に向けて新商品開発・新規顧客開拓を行った事例', updated_date: '2026-03-30 15:10' },
  ];

  const MAX_RESULTS = 4;
  let searchResults = null;
  let lastKeyword = '';

  function highlightText(text, keyword) {
    if (!keyword) return esc(text);
    const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(escapedKeyword, 'gi');
    let result = '';
    let lastIndex = 0;
    let m;
    while ((m = re.exec(text)) !== null) {
      result += esc(text.slice(lastIndex, m.index));
      result += `<mark>${esc(m[0])}</mark>`;
      lastIndex = m.index + m[0].length;
    }
    result += esc(text.slice(lastIndex));
    return result;
  }

  function formatKnowledgeBody(body, keyword) {
    const idx = body.indexOf('。');
    if (idx === -1) return highlightText(body, keyword);
    const lead = body.slice(0, idx + 1);
    const rest = body.slice(idx + 1);
    return `<strong>${highlightText(lead, keyword)}</strong>${rest ? `<br><br>${highlightText(rest, keyword)}` : ''}`;
  }

  function render() {
    root.innerHTML = `
      <div class="screen-body screen-body--fill">
        <div class="cat-lbl">🔍 検索条件を入力すると蓄積されたナレッジを検索できます</div>
        <div class="card" id="ks-search-card" style="margin-bottom:var(--space-6)">
          <div class="card-header card-header--navy"><div class="card-title card-title--white">🔍 検索条件</div></div>
          <div class="card-body" id="ks-search-header">
            <div class="flex items-end gap-md" style="width:100%;">
              <div class="filter-field" style="flex:1;">
                <div class="filter-field__label">検索したい内容</div>
                <input type="text" class="form-input" id="ks-keyword" placeholder="例：インボイス、賃上げ促進税制 など">
              </div>

              <div class="filter-field" style="align-self:stretch;">
                <div class="filter-field__label">&nbsp;</div>
                <button type="button" class="btn btn-primary--violet btn-sm" style="color:white; flex:1;" id="ks-search-btn">🔍 ナレッジを検索する</button>
              </div>
              <div class="filter-field" style="align-self:stretch;">
                <div class="filter-field__label">&nbsp;</div>
                <button type="button" class="btn btn-outline btn-sm" style="flex:1;" id="ks-clear-btn">✕ 検索内容をクリア</button>
              </div>
            </div>
          </div>
        </div>
        <div class="cat-lbl">
          <span>📚 検索結果<span id="ks-result-count" class="text-muted" style="font-weight:var(--fw-regular);margin-left:var(--space-3);"></span></span>
        </div>
        <div class="grid grid-gap-md" id="ks-results"></div>
      </div>
    `;
    const keywordEl = root.querySelector('#ks-keyword');
    root.querySelector('#ks-search-btn').addEventListener('click', runSearch);
    keywordEl.addEventListener('keydown', e => { if (e.key === 'Enter') runSearch(); });
    root.querySelector('#ks-clear-btn').addEventListener('click', () => {
      keywordEl.value = '';
      lastKeyword = '';
      searchResults = null;
      renderResults();
      keywordEl.focus();
    });
    renderResults();
    keywordEl.focus();
    if (typeof window.__applyRoleAccentColor === 'function') window.__applyRoleAccentColor();

    if (typeof alignCardBottomToManualInput === 'function') {
      requestAnimationFrame(() => {
        alignCardBottomToManualInput(root.querySelector('#ks-results'), false);
      });
    }
  }

  function runSearch() {
    const rawKeyword = root.querySelector('#ks-keyword').value.trim();
    const keyword = rawKeyword.toLowerCase();
    lastKeyword = rawKeyword;
    searchResults = keyword
      ? KNOWLEDGE_ENTRIES.filter(e => e.title.toLowerCase().includes(keyword) || e.content.toLowerCase().includes(keyword) || e.theme_label.toLowerCase().includes(keyword))
      : KNOWLEDGE_ENTRIES.slice();
    renderResults();
  }

  function renderResults() {
    const resultsEl = root.querySelector('#ks-results');
    const countEl = root.querySelector('#ks-result-count');
    if (!searchResults) {
      countEl.textContent = '';
      resultsEl.innerHTML = `<div class="text-muted text-sm" style="grid-column:1/-1">上の欄にキーワードを入力し「ナレッジを検索」を押してください。</div>`;
      return;
    }
    if (!searchResults.length) {
      countEl.textContent = '';
      resultsEl.innerHTML = `<div class="text-muted text-sm" style="grid-column:1/-1">該当するナレッジが見つかりませんでした。別のキーワードをお試しください。</div>`;
      return;
    }

    const shown = searchResults.slice(0, MAX_RESULTS);
    countEl.textContent = searchResults.length > shown.length
      ? `（上位${shown.length}件を表示）`
      : `（${shown.length}件）`;
    resultsEl.innerHTML = shown.map(e => `
      <div class="proposal-card proposal-card--mid">
        <div class="proposal-card__header">
          <div class="proposal-card__title">${highlightText(e.title, lastKeyword)}</div>
        </div>
        <div class="proposal-card__body">${formatKnowledgeBody(e.content, lastKeyword)}</div>
        <div class="proposal-card__meta"><span class="badge" style="--badge-color:${e.badge_color}">${esc(e.theme_label)}</span></div>
        <div class="proposal-card__meta" style="margin-top:var(--space-2)"><strong>📚 参照したナレッジ：</strong>${esc(e.code)}「${esc(e.title)}」<br><strong>🔍 参照した情報：</strong>${esc(e.ref_info)}</div>
        <div class="proposal-card__meta"><strong>更新日時：</strong>${esc(e.updated_date)}</div>
      </div>
    `).join('');
  }

  window.__renderKnowledgeSearch = () => { searchResults = null; lastKeyword = ''; render(); };
  render();
})();
