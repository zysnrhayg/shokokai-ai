(function () {
  const root = document.getElementById('ap-root');
  if (!root) return;

  const INDUSTRIES = [
    '卸売業、小売業', 'サービス業（他に分類されないもの）', '建設業', '宿泊業、飲食サービス業',
    '医療、福祉', '製造業', '生活関連サービス業、娯楽業', '不動産業、物品賃貸業', '運輸業、郵便業',
    '学術研究、専門・技術サービス業', '教育、学習支援業', '情報通信業', '金融業、保険業',
    '電気・ガス・熱供給・水道業', '農業、林業', '複合サービス事業', '漁業', '鉱業、採石業、砂利採取業',
    '公務（他に分類されるものを除く）', '分類不能の産業',
  ];
  const THEMES = [
    ['wage', '賃上げ・最低賃金引上げ'], ['labor', '省力化促進・人手不足'],
    ['energy', 'エネルギー価格・物価の高騰'], ['digital', 'デジタル化'], ['tariff', '米国関税'],
    ['invoice', 'インボイス制度'], ['ebooks', '電子帳簿保存法'], ['covid', '新型コロナ'],
    ['admin', '事業実施に係る事務処理'],
  ];
  const themeLabelByCode = new Map(THEMES.map(t => [t[0], t[1]]));

  const PROPOSAL_GIST_BY_TITLE = {
    '業務改善助成金の活用': '設備投資をすれば、資金負担を抑えながら最低賃金引き上げに対応できます',
    '価格転嫁支援・交渉支援': 'コスト上昇分を数字で示して交渉すれば、無理のない形で利益率を回復できます',
    '人材確保等支援助成金の活用': '助成金を活用すれば、賃金改善と生産性向上を無理なく進められます',
    '賃上げに伴う社会保険料負担の試算支援': '社会保険料の負担増を試算すれば、安心して賃上げに踏み切れます',
    '省力化投資による人件費削減': '省力化補助金で設備を導入すれば、人手不足に対応しながら人件費率を改善できます',
    '業務フロー見直し支援': '業務を棚卸しすれば、外部委託や自動化できる工程が見つかり効率化できます',
    'IT導入補助金によるツール導入': '受発注・在庫管理をITツールに置き換えれば、少人数でも業務が回る体制になります',
    '多能工化・兼務体制の整備支援': '1人が複数業務をこなせる体制をつくれば、急な欠員にも強くなります',
    '省エネ設備導入補助金の活用': '高効率空調やLED照明に切り替えれば、エネルギーコストを継続的に削減できます',
    'エネルギー使用状況の可視化診断': '専門家のエネルギー診断を受ければ、削減余地の大きい設備がわかります',
    '燃料費高騰対策の資金繰り相談': 'セーフティネット保証等を活用すれば、当面の資金繰りを安定させられます',
    '複数年契約による電力調達コスト見直し': '電力会社との契約を複数年契約に見直せば、調達コストの急な変動を抑えられます',
    'ECサイト構築・SNS活用支援': 'ECサイトとSNSで販路拡大を始めれば、新規顧客の獲得チャネルが増えます',
    '業務システムのクラウド化': '会計・受発注業務をクラウド化すれば、場所を選ばず業務ができるようになります',
    'キャッシュレス決済導入支援': 'キャッシュレス対応を進めれば、顧客の利便性が上がり機会損失を防げます',
    '社内DX人材の育成支援': '社内でデジタル人材を育てれば、外部に頼らず自走できる体制になります',
    '輸出先の多角化支援': '米国以外の輸出先も開拓すれば、関税リスクを一国に偏らせない体制がつくれます',
    'コスト増加分の価格転嫁相談': '関税負担分の価格交渉を専門家に相談すれば、無理のない形でコスト増を吸収できます',
    '為替・関税影響のシミュレーション支援': '関税率変動の影響を試算すれば、価格戦略の見直しに具体的に活かせます',
    '米国以外の販路開拓補助金の活用': '展示会出展を補助金でまかなえば、費用負担を抑えて新たな販路を試せます',
    'インボイス対応の経理体制整備': '請求書様式と会計ソフトを見直せば、インボイス制度への対応漏れがなくなります',
    '取引先との価格・契約条件の確認': '免税事業者との取引条件を確認すれば、認識のズレによるトラブルを防げます',
    '会計ソフト導入によるインボイス対応の効率化': '対応ソフトを導入すれば、日々の事務負担が減り対応漏れのリスクも下がります',
    '2割特例・簡易課税の適用検討': '2割特例や簡易課税の適用を確認すれば、納税負担を軽減できる可能性があります',
    '電子帳簿保存法対応の体制整備': '保存ルールを専門家と整備すれば、法令の保存要件を満たしながら運用をシンプルにできます',
    'スキャナ保存制度の活用検討': '紙の書類をスキャナ保存に切り替えれば、保管スペースが減り必要な書類もすぐ検索できます',
    '会計システムのタイムスタンプ対応確認': 'タイムスタンプ要件を確認すれば、改ざん防止の要件を確実にクリアできます',
    '電子取引データの保存規程整備支援': '保存規程を整備すれば、誰が対応しても同じ運用ができ属人化を防げます',
    '売上回復に向けた販路開拓支援': '新商品・新サービスを考えれば、専門家の支援を受けながら新しい販路開拓につなげられます',
    'コロナ融資の借換・返済条件見直し相談': '返済条件を見直せば、借換保証制度等で月々の返済負担を軽くできる可能性があります',
    '事業再構築による新分野展開支援': '新分野展開や業態転換を検討すれば、補助金を活用しながら新しい柱をつくれます',
    'BCP（事業継続計画）策定支援': 'BCPを専門家と策定すれば、いざという時も事業を止めずに続けられます',
  };
  const PROPOSAL_ORDER_LABELS = ['一つ目の提案', '二つ目の提案', '三つ目の提案', '四つ目の提案'];

  const WAGE_TEMPLATES = [
    { title: '業務改善助成金の活用', body: '業務改善助成金を活用して、設備投資を行ってみませんか。これなら、最大9/10の補助率で対応でき、資金負担を抑えながら最低賃金引き上げに対応できます（同業種での活用実績12件あり）。申請書類の作成から生産性向上計画の策定まで、商工会の窓口で一緒に整理しながら進められるため、初めての申請でも安心して取り組めます。', meta: '関連補助金：業務改善助成金 / 対象：全業種 / 補助率：最大9/10' },
    { title: '価格転嫁支援・交渉支援', body: '原材料費や人件費の上昇分を算出し、その根拠資料をそろえたうえで取引先へ値上げを打診してみませんか。コスト上昇の内訳を数字で示しながら交渉することで、価格改定について取引先の理解を得やすくなり、無理のない形で利益率を回復できます。交渉の切り出し方や想定される反論への返し方まで専門家が具体的にアドバイスするため、値上げ交渉に不慣れな場合でも落ち着いて対応できます。', meta: '関連施策：中小企業庁 価格転嫁促進策' },
    { title: '人材確保等支援助成金の活用', body: '人材確保等支援助成金を活用してみませんか。これなら、賃金改善と生産性向上の制度導入を進めながら、助成金で費用の一部をまかなえます。就業規則の見直しや評価制度の設計といった実務面も専門家がサポートするため、制度導入後の運用まで見据えて無理なく進められます。', meta: '関連助成金：人材確保等支援助成金（雇用管理制度助成コース）' },
    { title: '賃上げに伴う社会保険料負担の試算支援', body: '賃上げ前に、社会保険料の負担増を試算しておきませんか。これなら、資金繰り計画への影響が事前に見えるので、安心して賃上げに踏み切れます。従業員一人ひとりの等級変更まで含めたシミュレーションを社会保険労務士が作成するため、賃上げ幅の妥当性も具体的な数字で検討できます。', meta: '関連施策：社会保険労務士による経営相談' },
  ];
  const LABOR_TEMPLATES = [
    { title: '省力化投資による人件費削減', body: '省力化補助金（カタログ型）で設備を導入してみませんか。これなら、1人当たりの生産性が上がり、人件費率を改善しながら人手不足にも対応できます。カタログに掲載された汎用製品から選ぶだけで申請できる仕組みのため、大掛かりな計画書作成の負担なく、短期間での導入を目指せます。', meta: '関連補助金：中小企業省力化投資補助金' },
    { title: '業務フロー見直し支援', body: '既存業務を一度棚卸ししてみませんか。これなら、外部委託や自動化できる工程が見つかり、専門家派遣を使って無理なく効率化できます。現場の作業を実際に観察したうえで改善提案を受けられるため、机上の空論ではない、実行しやすい業務フローに組み替えられます。', meta: '関連施策：専門家派遣事業' },
    { title: 'IT導入補助金によるツール導入', body: '受発注・在庫管理をITツールに置き換えてみませんか。これなら、少人数でも業務が回る体制になり、補助金で導入コストも抑えられます。ツール選定から操作研修までIT導入支援事業者が伴走するため、パソコン操作に不慣れな従業員がいても安心して移行できます。', meta: '関連補助金：IT導入補助金（通常枠）' },
    { title: '多能工化・兼務体制の整備支援', body: '1人が複数業務をこなせる体制づくりを進めてみませんか。これなら、限られた人員でも業務が回るようになり、急な欠員にも強くなります。業務ごとの習熟度を見える化したスキルマップを作成することで、誰が何を学べば体制が強化できるか計画的に育成を進められます。', meta: '関連施策：人材開発支援助成金' },
  ];
  const ENERGY_TEMPLATES = [
    { title: '省エネ設備導入補助金の活用', body: '高効率空調やLED照明への切り替えを検討してみませんか。これなら、エネルギーコストを継続的に削減でき、補助金で初期投資の負担も軽くなります。導入前後の電気使用量を比較した費用対効果の試算も専門家に依頼できるため、投資回収の見通しを立てたうえで判断できます。', meta: '関連補助金：省エネルギー投資促進支援事業費補助金' },
    { title: 'エネルギー使用状況の可視化診断', body: 'まずは専門家によるエネルギー診断を受けてみませんか。これなら、削減余地の大きい設備が具体的にわかり、優先順位をつけて対策できます。診断結果は数値と改善提案をまとめたレポートとして受け取れるため、その後の補助金申請や設備更新計画の根拠資料としても活用できます。', meta: '関連施策：省エネルギー診断事業' },
    { title: '燃料費高騰対策の資金繰り相談', body: '燃料費・電気代高騰による資金繰りを専門家に相談してみませんか。これなら、セーフティネット保証等を活用でき、当面の資金繰りを安定させられます。金融機関への説明資料の作成も一緒に進められるため、融資審査に必要な準備を効率よく整えられます。', meta: '関連施策：セーフティネット保証4号・5号' },
    { title: '複数年契約による電力調達コスト見直し', body: '電力会社との契約プランを見直してみませんか。これなら、複数年契約で単価を固定でき、調達コストの急な変動を抑えられます。複数の電力会社から見積もりを取り寄せて比較する段階から相談できるため、自社の使用パターンに合った契約を選びやすくなります。', meta: '関連施策：省エネルギー相談窓口' },
  ];
  const PROPOSAL_TEMPLATES = {
    wage: WAGE_TEMPLATES, labor: LABOR_TEMPLATES, energy: ENERGY_TEMPLATES,
    digital: [
      { title: 'ECサイト構築・SNS活用支援', body: 'ECサイトとSNSを使った販路拡大を始めてみませんか。これなら、新規顧客の獲得チャネルが増え、専門家のハンズオン支援で無理なく運用を軌道に乗せられます。商品撮影や投稿文の作り方といった実践的なノウハウも学べるため、開設後の運用を自社だけで続けられる体制を目指せます。', meta: '関連補助金：小規模事業者持続化補助金（デジタル枠）' },
      { title: '業務システムのクラウド化', body: '会計・受発注業務をクラウドシステムに移してみませんか。これなら、場所を選ばず業務ができるようになり、日々の業務効率が上がります。既存の紙帳簿やExcel管理からの移行手順も専門家がサポートするため、データの引き継ぎ漏れを防ぎながら安心して切り替えられます。', meta: '関連施策：IT導入補助金' },
      { title: 'キャッシュレス決済導入支援', body: 'QRコード決済などのキャッシュレス対応を進めてみませんか。これなら、顧客の利便性が上がって機会損失を防げ、導入費用も一部補助を受けられます。複数の決済手段の手数料や入金サイクルを比較したうえで自社に合ったものを選べるため、導入後のコスト負担も見通しやすくなります。', meta: '関連施策：キャッシュレス決済導入支援' },
      { title: '社内DX人材の育成支援', body: '社内でデジタルツールを使いこなせる人を育ててみませんか。これなら、外部に頼らず自走できる体制ができ、長期的なコスト削減にもつながります。研修プログラムは基礎から実務課題への応用まで段階的に組まれているため、ITが苦手な従業員でも無理なくスキルアップできます。', meta: '関連施策：人材開発支援助成金（DXコース）' },
    ],
    tariff: [
      { title: '輸出先の多角化支援', body: '米国以外の輸出先も開拓してみませんか。これなら、商談会・海外展示会への出展を通じて、関税リスクを一国に偏らせない体制がつくれます。現地バイヤーとのマッチングから商談後のフォローまで専門家が伴走するため、初めての新規国開拓でも着実に進められます。', meta: '関連施策：JETRO 新規輸出1万者支援プログラム' },
      { title: 'コスト増加分の価格転嫁相談', body: '関税負担増加分について、取引先との価格交渉を専門家に相談してみませんか。これなら、交渉の進め方が整理でき、無理のない形でコスト増を吸収できます。関税分の算定根拠を明確にした説明資料の作成もサポートを受けられるため、取引先にも納得してもらいやすい交渉が可能です。', meta: '関連施策：価格転嫁サポート窓口' },
      { title: '為替・関税影響のシミュレーション支援', body: '関税率の変動が採算に与える影響を試算してみませんか。これなら、リスクの大きさが数字で見え、価格戦略の見直しに具体的に活かせます。為替レートの変動シナリオも組み合わせた複数パターンの試算を行うため、今後の事業計画により幅を持たせて備えられます。', meta: '関連施策：中小企業海外展開支援' },
      { title: '米国以外の販路開拓補助金の活用', body: '新規販路開拓の展示会出展を補助金でまかなってみませんか。これなら、費用負担を抑えながら、米国以外の新たな販路を試せます。出展計画書の作成から補助金の実績報告まで一連の手続きを専門家がサポートするため、初めての補助金活用でも安心です。', meta: '関連補助金：小規模事業者持続化補助金（販路開拓枠）' },
    ],
    invoice: [
      { title: 'インボイス対応の経理体制整備', body: '請求書様式と会計ソフトの設定を専門家と一緒に見直してみませんか。これなら、インボイス制度への対応漏れがなくなり、経理業務も安定します。適格請求書発行事業者としての登録状況の確認から日々の記帳ルールの整備まで、実務に即した形でサポートを受けられます。', meta: '関連施策：インボイス制度定着支援窓口' },
      { title: '取引先との価格・契約条件の確認', body: '免税事業者との取引条件を一度確認してみませんか。これなら、認識のズレによるトラブルを事前に防げます。取引先ごとの状況を整理したチェックリストを作成することで、優先的に確認すべき相手先から順に対応を進められます。', meta: '関連施策：下請Gメンヒアリング事例集' },
      { title: '会計ソフト導入によるインボイス対応の効率化', body: 'インボイス対応の会計・請求書ソフトを導入してみませんか。これなら、日々の事務負担が減り、対応漏れのリスクも下がります。既存の請求書フォーマットを踏まえたソフト選定のアドバイスも受けられるため、導入後の業務フローの変化を最小限に抑えられます。', meta: '関連補助金：IT導入補助金（インボイス枠）' },
      { title: '2割特例・簡易課税の適用検討', body: '2割特例や簡易課税制度が使えないか、専門家に確認してみませんか。これなら、免税事業者からの転換に伴う納税負担を軽減できる可能性があります。自社の売上構成や経費の内容を踏まえたうえでどちらの制度が有利か試算してもらえるため、納得したうえで選択できます。', meta: '関連施策：インボイス制度負担軽減措置' },
    ],
    ebooks: [
      { title: '電子帳簿保存法対応の体制整備', body: '電子取引データの保存ルールを専門家と一緒に整備してみませんか。これなら、法令の保存要件を満たしながら、日々の運用もシンプルにできます。取引先とのメールやクラウド上でのやり取りも含めた保存対象の洗い出しから一緒に進められるため、対応漏れを防げます。', meta: '関連施策：IT導入補助金（電子帳簿保存法対応類型）' },
      { title: 'スキャナ保存制度の活用検討', body: '紙の請求書・領収書をスキャナ保存に切り替えてみませんか。これなら、書類の保管スペースが減り、必要な書類もすぐ検索できるようになります。導入にあたって必要なタイムスタンプ要件や運用規程の整備も併せて相談できるため、法令に沿った形で移行できます。', meta: '関連施策：電子帳簿保存法（スキャナ保存制度）' },
      { title: '会計システムのタイムスタンプ対応確認', body: '今のシステムがタイムスタンプ要件を満たしているか確認してみませんか。これなら、改ざん防止の要件を確実にクリアでき、安心して電子保存に移行できます。要件を満たしていない場合の代替システムの選び方まで含めて相談できるため、移行に伴う手戻りを防げます。', meta: '関連施策：電子帳簿保存法 検索要件チェック' },
      { title: '電子取引データの保存規程整備支援', body: '電子取引データの取り扱いを社内規程として整備してみませんか。これなら、誰が対応しても同じ運用ができるようになり、属人化を防げます。規程のひな形をもとに自社の業務フローに合わせてカスタマイズできるため、実態に即した無理のないルールづくりが可能です。', meta: '関連施策：国税庁 電子帳簿保存法一問一答' },
    ],
    covid: [
      { title: '売上回復に向けた販路開拓支援', body: 'コロナ後の需要変化に合わせた新商品・新サービスを考えてみませんか。これなら、専門家の支援を受けながら、新しい販路開拓につなげられます。市場調査から試作品づくり、テスト販売までの一連のプロセスを段階的に伴走してもらえるため、着実に成果へつなげられます。', meta: '関連施策：小規模事業者持続化補助金' },
      { title: 'コロナ融資の借換・返済条件見直し相談', body: 'コロナ関連融資の返済条件を見直してみませんか。これなら、借換保証制度等を使って、月々の返済負担を軽くできる可能性があります。複数の借入をまとめて借り換える際の資金繰り計画も一緒に作成できるため、無理のない返済スケジュールを組み直せます。', meta: '関連施策：伴走支援型特別保証制度' },
      { title: '事業再構築による新分野展開支援', body: 'この機会に新分野展開や業態転換を検討してみませんか。これなら、補助金を活用しながら、事業環境の変化に合わせた新しい柱をつくれます。事業計画書の策定には認定支援機関のサポートを受けられるため、採択に向けた説得力のある計画に仕上げられます。', meta: '関連補助金：事業再構築補助金' },
      { title: 'BCP（事業継続計画）策定支援', body: '感染症の再拡大に備えたBCPを専門家と一緒に策定してみませんか。これなら、いざという時も事業を止めずに続けられる備えができます。策定後の訓練や見直しのサイクルまで含めて伴走支援を受けられるため、計画を作って終わりにせず実効性を高められます。', meta: '関連施策：中小企業BCP策定運用指針' },
    ],
  };

  let proposals = [];
  let summaryText = '';
  let lastThemeCodes = [];
  let altOffset = 0;

  function render() {
    root.innerHTML = `
      <div class="screen-body">
        <div class="grid grid-form-result grid-gap-lg">
          <div>
            <div class="card">
              <div class="card-header card-header--navy"><div class="card-title card-title--white">✏️ お困りのことやご相談内容をお聞かせください</div></div>
              <div class="card-body">
                <div class="form-grid" id="ap-form-grid">
                  <div class="form-row">
                    <textarea class="form-input" id="ap-summary" rows="6" placeholder="事業者の状況・相談内容を入力">最低賃金引き上げ対応で人件費が増加。売上は横ばいで財源確保に悩んでいる。価格転嫁も検討中。</textarea>
                  </div>
                  <div class="flex items-center gap-sm" style="justify-content:flex-end;">
                    <button type="button" class="btn btn-outline btn-sm" id="ap-clear">✕ 入力内容をクリア</button>
                    <button type="button" class="btn btn-primary--violet btn-sm" id="ap-generate">✨ AIに提案してもらう</button>
                  </div>
                  <div style="font-size:var(--fs-md);color:var(--text);margin-top:1.5em">ご希望や条件を詳しく教えていただくと、あなたに合った提案ができます。</div>
                  <div class="form-row"><div class="form-label" style="white-space:nowrap">事業所名／業種</div>
                    <div class="flex items-center gap-sm">
                      <div class="mi-autocomplete" style="flex:1; min-width:160px;">
                        <input type="text" class="form-input" id="ap-business-name" placeholder="事業所名を入力" autocomplete="off">
                        <div class="mi-autocomplete__dropdown" id="ap-business-dropdown"></div>
                      </div>
                      <select class="form-input" id="ap-industry" style="max-width:280px"><option value="">業種を選択</option>${INDUSTRIES.map(i => `<option value="${esc(i)}">${esc(i)}</option>`).join('')}</select>
                    </div>
                  </div>
                  <div class="form-row"><div class="form-label" style="white-space:nowrap">支援テーマ（複数選択可）</div>
                    <div class="checkbox-grid">${THEMES.map(t => `<label><input type="checkbox" class="ap-theme-checkbox" value="${esc(t[0])}"> ${esc(t[1])}</label>`).join('')}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <div class="card" id="ap-result-card">
              <div class="card-header" id="ap-result-header"><div class="card-title" id="ap-result-title">こちらの提案内容はいかがでしょうか。</div></div>
              <div class="flex-col gap-lg" style="padding:var(--space-5)" id="ap-result-body"></div>
            </div>
          </div>
        </div>
      </div>
    `;
    renderResult();
    root.querySelector('#ap-generate').addEventListener('click', generate);
    root.querySelector('#ap-clear').addEventListener('click', () => {
      root.querySelector('#ap-summary').value = '';
      root.querySelector('#ap-business-name').value = '';
      root.querySelector('#ap-industry').value = '';
      root.querySelectorAll('.ap-theme-checkbox').forEach(cb => { cb.checked = false; });
      proposals = [];
      summaryText = '';
      lastThemeCodes = [];
      altOffset = 0;
      renderResult();
    });

    SelectWidth.fit(root.querySelector('#ap-industry'));
    if (typeof window.__applyRoleAccentColor === 'function') window.__applyRoleAccentColor();
    wireBusinessNameSuggest();
    root.querySelector('#ap-summary').focus();
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

  function wireBusinessNameSuggest() {
    const input = root.querySelector('#ap-business-name');
    const dropdown = root.querySelector('#ap-business-dropdown');
    if (!input || !dropdown) return;
    let timer = null;
    let seq = 0;

    function renderMatches(names) {
      dropdown.innerHTML = '';
      if (!names.length) {
        const empty = document.createElement('div');
        empty.className = 'mi-autocomplete__item mi-autocomplete__item--empty';
        empty.textContent = '候補がありません';
        dropdown.appendChild(empty);
        return;
      }
      names.forEach(function (name) {
        const item = document.createElement('div');
        item.className = 'mi-autocomplete__item';
        item.textContent = name;
        item.addEventListener('mousedown', function (e) {
          e.preventDefault();
          input.value = name;
          dropdown.classList.remove('is-open');
        });
        dropdown.appendChild(item);
      });
    }

    function search() {
      const q = input.value.trim();
      if (!q) {
        dropdown.classList.remove('is-open');
        return;
      }
      const my = ++seq;
      clearTimeout(timer);
      timer = setTimeout(function () {
        const body = Object.assign({
          keyword: q,
          xx: q,
          limit: '20',
        }, (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {});
        postAp('./jigyoshomeinokohokakonosodanrirekinamesapi.do', body).then(function (result) {
          if (my !== seq) return;
          const data = (result && result.data) || {};
          if (data.e) {
            renderMatches([]);
            dropdown.classList.add('is-open');
            return;
          }
          const names = parseDragB(data).map(function (r) {
            return (r && (r.business_name || r.businessname)) || '';
          }).filter(Boolean);
          renderMatches(names);
          dropdown.classList.add('is-open');
        }).catch(function () {
          if (my !== seq) return;
          renderMatches([]);
          dropdown.classList.add('is-open');
        });
      }, 280);
    }

    input.addEventListener('input', search);
    input.addEventListener('focus', search);
    input.addEventListener('blur', function () {
      setTimeout(function () { dropdown.classList.remove('is-open'); }, 150);
    });
  }

  function applyApiIndustries(rows) {
    const select = root.querySelector('#ap-industry');
    if (!select || !Array.isArray(rows) || !rows.length) return;
    const prev = select.value;
    const opts = ['<option value=\"\">業種を選択</option>'].concat(rows.map(function (r) {
      const label = String(r.label || '').trim();
      const code = String(r.industry_code || '').trim();
      if (!label) return '';
      // value=label for generate keyword; keep code in data attribute
      return `<option value="${esc(label)}" data-code="${esc(code)}">${esc(label)}</option>`;
    }).filter(Boolean));
    select.innerHTML = opts.join('');
    if (prev && select.querySelector('option[value=\"' + prev.replace(/\"/g, '\\\"') + '\"]')) {
      select.value = prev;
    }
    SelectWidth.fit(select);
  }

  function postAp(url, body) {
    if (window.ApiClient && typeof window.ApiClient.post === 'function') {
      return window.ApiClient.post(url, body);
    }
    return Promise.reject(new Error('ApiClient unavailable'));
  }

  function applyApiThemes(themeRows) {
    if (!Array.isArray(themeRows) || !themeRows.length) return;
    const grid = root.querySelector('.checkbox-grid');
    if (!grid) return;
    const items = themeRows.map(function (t) {
      // Prefer theme_code (wage/labor/...). Never use badge_class color as value.
      const code = String(t.theme_code || t.filter_group || '').trim();
      const label = String(t.label || code).trim();
      if (!code || code.charAt(0) === '#') return null;
      themeLabelByCode.set(code, label);
      return [code, label];
    }).filter(Boolean);
    if (!items.length) return;
    grid.innerHTML = items.map(function (t) {
      return `<label><input type="checkbox" class="ap-theme-checkbox" value="${esc(t[0])}"> ${esc(t[1])}</label>`;
    }).join('');
  }

  function selectedThemeLabels(codes) {
    return (codes || []).map(function (c) { return themeLabelByCode.get(c) || c; }).filter(Boolean);
  }

  function generate() {
    const industry = root.querySelector('#ap-industry').value;
    const themeCodes = Array.from(root.querySelectorAll('.ap-theme-checkbox:checked')).map(cb => cb.value);
    const themeLabel = themeCodes.map(c => themeLabelByCode.get(c) || c).join('、');
    const summary = root.querySelector('#ap-summary').value.trim();
    if (!summary) {
      Toast.error('相談概要が未入力です。ご確認ください');
      return;
    }

    lastThemeCodes = themeCodes.length ? themeCodes : ['wage'];
    altOffset = 0;
    const labels = selectedThemeLabels(lastThemeCodes);
    const themeLabelForApi = labels.join('、') || themeLabel;
    summaryText = `ご相談内容の整理：${industry}を営む事業者様より「${themeLabelForApi}」に関するご相談です。「${summary}」とのことですので、この内容をもとに以下の支援策をご提案します。`;

    const body = Object.assign({
      industry: industry,
      // Send Japanese labels so DB ILIKE can hit knowledge titles/content
      themefiltergroup: themeLabelForApi,
      consultationsummary: summary,
    }, (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {});

    postAp('./aiproposalgenerateapi.do', body).then(function (result) {
      const data = (result && result.data) || {};
      if (Array.isArray(data.proposals) && data.proposals.length) {
        proposals = data.proposals;
        renderResult();
        Toast.success(data.i || 'AI提案を生成しました');
      } else {
        proposals = [];
        renderResult();
        Toast.error(data.e || '該当するナレッジ提案が見つかりませんでした');
      }
      logAiUsage(
        '/ai-proposal/log-usage', '', 'ai_proposal.generate',
        `業種: ${industry} / 支援テーマ: ${themeLabel} / 相談概要: ${summary}`,
        proposals.map(p => `${p.title}\n${p.body}`).join('\n\n')
      );
    }).catch(function () {
      proposals = [];
      renderResult();
      Toast.error('提案の生成に失敗しました');
    });
  }

  function showAlternate(reason) {
    if (!lastThemeCodes.length) return;
    altOffset += 2;
    const themeLabelForApi = selectedThemeLabels(lastThemeCodes).join('、') || lastThemeCodes[0] || '';
    const body = Object.assign({
      reason: reason || '',
      themefiltergroup: themeLabelForApi,
    }, (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {});

    postAp('./aiproposalregenerateapi.do', body).then(function (result) {
      const data = (result && result.data) || {};
      if (Array.isArray(data.proposals) && data.proposals.length) {
        proposals = data.proposals;
      } else {
        proposals = [];
      }
      renderResult();
      if (proposals.length) {
        Toast.success(data.i || (reason ? `「${reason}」を踏まえて別の提案を表示しました` : '別の提案を表示しました'));
      } else {
        Toast.error(data.e || '代替提案が見つかりませんでした');
      }
    }).catch(function () {
      proposals = [];
      renderResult();
      Toast.error('代替提案の取得に失敗しました');
    });
  }

  function loadInit() {
    const body = (window.ApiClient && window.ApiClient.orgContext) ? window.ApiClient.orgContext() : {};
    postAp('./aiproposalinitapi.do', body).then(function (result) {
      const data = (result && result.data) || {};
      if (data.e) return;
      applyApiThemes(data.themes);
      applyApiIndustries(data.industries);
    }).catch(function () { /* keep local themes / industries */ });
  }

  function formatProposalBody(body) {
    const idx = body.indexOf('。');
    if (idx === -1) return esc(body);
    const lead = body.slice(0, idx + 1);
    const rest = body.slice(idx + 1);
    return `<strong>${esc(lead)}</strong>${rest ? `<br><br>${esc(rest)}` : ''}`;
  }

  function renderResult() {
    const titleEl = root.querySelector('#ap-result-title');
    const bodyEl = root.querySelector('#ap-result-body');
    if (!titleEl || !bodyEl) return;
    titleEl.textContent = 'こちらの提案内容はいかがでしょうか。';
    const fallbackReferenceLine = '<strong>📚 参照したナレッジ：</strong>該当する公開ナレッジがありません（一般知識に基づく提案です）';

    const KNOWLEDGE_REF_BY_THEME = {
      wage: { title: 'K-014「業務改善助成金 活用事例集」', info: '同業種が本助成金を活用した際の申請書類の書き方・生産性向上計画の記載例' },
      labor: { title: 'K-021「省力化投資による人手不足対応 事例集」', info: '省力化補助金で設備を導入し人手不足を解消した中小企業の事例' },
      energy: { title: 'K-018「省エネ設備導入 補助金活用ガイド」', info: '空調・照明等の省エネ設備導入で使える補助金の対象要件と申請の流れ' },
      digital: { title: 'K-026「小規模事業者のデジタル化支援まとめ」', info: '小規模事業者がITツールを導入する際に使える支援策の一覧と選び方' },
      tariff: { title: 'K-031「米国関税影響を踏まえた販路多角化事例」', info: '米国向け輸出に依存していた事業者が販路を多角化した進め方' },
      invoice: { title: 'K-009「インボイス制度 対応チェックリスト」', info: 'インボイス制度対応で確認すべき請求書様式・経理体制のチェック項目' },
      ebooks: { title: 'K-011「電子帳簿保存法 対応の手引き」', info: '電子帳簿保存法で求められる保存要件と社内体制整備のポイント' },
      covid: { title: 'K-005「コロナ後の販路回復支援事例集」', info: 'コロナ後の販路回復に向けて新商品開発・新規顧客開拓を行った事例' },
    };
    const knowledgeRef = KNOWLEDGE_REF_BY_THEME[lastThemeCodes[0]];
    const firstReferenceLine = knowledgeRef
      ? `<strong>📚 参照したナレッジ：</strong>${esc(knowledgeRef.title)}<br><strong>🔍 参照した情報：</strong>${esc(knowledgeRef.info)}`
      : fallbackReferenceLine;

    const roleSelectEl = document.getElementById('org-role-select');
    const currentRole = roleSelectEl ? roleSelectEl.value : 'shokokai';
    const isFederationNow = currentRole === 'national' || currentRole === 'pref';
    const proposalsHtml = proposals.map((p, i) => {
      const apiMeta = (p.meta || p.knowledge_code)
        ? `<strong>📚 参照したナレッジ：</strong>${esc(p.meta || ('関連ナレッジ：' + p.knowledge_code))}`
        : '';
      const metaLine = apiMeta || (i === 0 ? firstReferenceLine : fallbackReferenceLine);
      return `
      <div class="proposal-card">
        <div class="proposal-card__header">
          <div class="proposal-card__title"><span style="margin-right:var(--space-3);white-space:nowrap;">${esc(PROPOSAL_ORDER_LABELS[i] || `${i + 1}件目の提案`)}</span>${esc(PROPOSAL_GIST_BY_TITLE[p.title] || p.title)}</div>
        </div>
        <div class="proposal-card__body">${formatProposalBody(p.body)}</div>
        <div class="proposal-card__meta">${metaLine}</div>
        ${isFederationNow ? '' : `
        <div class="flex items-center" style="justify-content:flex-end;">
          <button type="button" class="btn btn-primary--violet btn-sm mt-sm ap-apply-btn" data-index="${i}" style="color:white">提案内容から報告書を作成する</button>
        </div>`}
      </div>
    `;
    }).join('');

    const differentHtml = proposals.length ? `
      <div style="margin-top:var(--space-4);">
        <div style="font-size:var(--fs-md);color:var(--text);margin-bottom:var(--space-2);">今回の提案内容は、ご希望に合っていますか？気になる点があれば、お聞かせください。</div>
        <div class="flex items-center gap-md">
          <input type="text" class="form-input" id="ap-different-reason" placeholder="何が違いますか？（任意）" style="flex:1;">
          <button type="button" class="btn btn-outline btn-sm" id="ap-different-submit" style="white-space:nowrap;">✗ 違う提案を見る</button>
        </div>
      </div>
    ` : '';

    bodyEl.innerHTML = proposals.length
      ? proposalsHtml + differentHtml
      : `<div style="font-size:var(--fs-md);color:var(--text)">まだAI提案は生成されていません。左のフォームを入力し「AI提案を生成」を押してください。</div>`;

    if (proposals.length) {
      const submitBtn = root.querySelector('#ap-different-submit');
      if (submitBtn) submitBtn.addEventListener('click', () => {
        const reason = root.querySelector('#ap-different-reason').value.trim();
        showAlternate(reason);
      });
      root.querySelectorAll('.ap-apply-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const p = proposals[Number(btn.dataset.index)];

          const businessName = root.querySelector('#ap-business-name').value.trim();
          window.__miPendingPrefill = { content: `${p.title}\n${p.body}`, themeCodes: lastThemeCodes, businessName };
          location.hash = '#manual-input';
        });
      });
    }
  }

  window.__renderAiProposal = () => {
    proposals = [];
    summaryText = '';
    lastThemeCodes = [];
    altOffset = 0;
    render();
    loadInit();
  };
  render();
  loadInit();
})();
