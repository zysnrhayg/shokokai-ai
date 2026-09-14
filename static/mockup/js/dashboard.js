(function () {
  const root = document.getElementById('home-federation-content');
  if (!root) return;

  const THEMES = [
    { code: 'wage', label: '賃上げ・最低賃金引上げ', count: 42 },
    { code: 'laborshort', label: '省力化促進・人手不足', count: 35 },
    { code: 'energy', label: 'エネルギー価格・物価の高騰', count: 21 },
    { code: 'digital', label: 'デジタル化', count: 18 },
    { code: 'tariff', label: '米国関税', count: 9 },
    { code: 'invoice', label: 'インボイス制度', count: 14 },
    { code: 'ebooks', label: '電子帳簿保存法', count: 6 },
    { code: 'covid', label: '新型コロナ', count: 3 },
  ];

  const TIER_CYCLE = ['h5', 'h4', 'h3', 'h2', 'h1'];

  function tierForIndex(i, nameLength) {
    return TIER_CYCLE[((i * 37 + nameLength * 13) % 23) % TIER_CYCLE.length];
  }
  const SHOKOKAI_ROWS = [
    ['2001','石狩北商工会','石狩北',1,'石狩'],['2002','北広島商工会','北広島',1,'石狩'],
    ['2003','当別町商工会','当別町',1,'石狩'],['2004','新篠津村商工会','新篠津村',1,'石狩'],
    ['2005','函館東商工会','函館東',1,'石狩'],['2006','函館市亀田商工会','函館市亀田',1,'石狩'],
    ['2007','北斗市商工会','北斗市',1,'石狩'],['2008','松前商工会','松前',1,'石狩'],
    ['2009','福島町商工会','福島町',1,'石狩'],['2010','知内商工会','知内',1,'石狩'],
    ['2011','木古内商工会','木古内',1,'石狩'],
    ['2012','七飯町商工会','七飯町',2,'渡島'],['2013','鹿部商工会','鹿部',2,'渡島'],
    ['2014','森町さわら商工会','森町さわら',2,'渡島'],['2015','八雲商工会','八雲',2,'渡島'],
    ['2016','長万部商工会','長万部',2,'渡島'],['2017','江差商工会','江差',2,'渡島'],
    ['2018','上ノ国町商工会','上ノ国町',2,'渡島'],['2019','厚沢部商工会','厚沢部',2,'渡島'],
    ['2020','乙部町商工会','乙部町',2,'渡島'],['2021','奥尻商工会','奥尻',2,'渡島'],
    ['2022','今金町商工会','今金町',2,'渡島'],
    ['2023','せたな商工会','せたな',3,'檜山'],['2024','島牧商工会','島牧',3,'檜山'],
    ['2025','寿都商工会','寿都',3,'檜山'],['2026','黒松内町商工会','黒松内町',3,'檜山'],
    ['2027','蘭越町商工会','蘭越町',3,'檜山'],['2028','ニセコ町商工会','ニセコ町',3,'檜山'],
    ['2029','真狩村商工会','真狩村',3,'檜山'],['2030','留寿都商工会','留寿都',3,'檜山'],
    ['2031','喜茂別町商工会','喜茂別町',3,'檜山'],['2032','京極町商工会','京極町',3,'檜山'],
    ['2033','共和町商工会','共和町',3,'檜山'],
    ['2034','泊村商工会','泊村',4,'後志'],['2035','神恵内村商工会','神恵内村',4,'後志'],
    ['2036','積丹町商工会','積丹町',4,'後志'],['2037','古平町商工会','古平町',4,'後志'],
    ['2038','仁木町商工会','仁木町',4,'後志'],['2039','赤井川村商工会','赤井川村',4,'後志'],
    ['2040','いわみざわ商工会','いわみざわ',4,'後志'],['2041','三笠市商工会','三笠市',4,'後志'],
    ['2042','江部乙商工会','江部乙',4,'後志'],['2043','南幌町商工会','南幌町',4,'後志'],
    ['2044','奈井江町商工会','奈井江町',4,'後志'],
    ['2045','由仁町商工会','由仁町',5,'空知'],['2046','長沼町商工会','長沼町',5,'空知'],
    ['2047','月形商工会','月形',5,'空知'],['2048','浦臼町商工会','浦臼町',5,'空知'],
    ['2049','新十津川町商工会','新十津川町',5,'空知'],['2050','妹背牛商工会','妹背牛',5,'空知'],
    ['2051','秩父別町商工会','秩父別町',5,'空知'],['2052','雨竜町商工会','雨竜町',5,'空知'],
    ['2053','北竜町商工会','北竜町',5,'空知'],['2054','沼田町商工会','沼田町',5,'空知'],
    ['2055','あさひかわ商工会','あさひかわ',5,'空知'],
    ['2056','山部商工会','山部',6,'上川'],['2057','鷹栖町商工会','鷹栖町',6,'上川'],
    ['2058','東神楽町商工会','東神楽町',6,'上川'],['2059','当麻町商工会','当麻町',6,'上川'],
    ['2060','比布商工会','比布',6,'上川'],['2061','愛別商工会','愛別',6,'上川'],
    ['2062','上川町商工会','上川町',6,'上川'],['2063','東川町商工会','東川町',6,'上川'],
    ['2064','美瑛町商工会','美瑛町',6,'上川'],['2065','上富良野町商工会','上富良野町',6,'上川'],
    ['2066','中富良野町商工会','中富良野町',6,'上川'],
    ['2067','南富良野町商工会','南富良野町',7,'留萌'],['2068','占冠村商工会','占冠村',7,'留萌'],
    ['2069','和寒町商工会','和寒町',7,'留萌'],['2070','剣渕商工会','剣渕',7,'留萌'],
    ['2071','朝日商工会','朝日',7,'留萌'],['2072','風連商工会','風連',7,'留萌'],
    ['2073','下川町商工会','下川町',7,'留萌'],['2074','美深町商工会','美深町',7,'留萌'],
    ['2075','音威子府村商工会','音威子府村',7,'留萌'],['2076','中川町商工会','中川町',7,'留萌'],
    ['2077','幌加内町商工会','幌加内町',8,'宗谷'],['2078','増毛町商工会','増毛町',8,'宗谷'],
    ['2079','小平町商工会','小平町',8,'宗谷'],['2080','苫前町商工会','苫前町',8,'宗谷'],
    ['2081','羽幌町商工会','羽幌町',8,'宗谷'],['2082','初山別村商工会','初山別村',8,'宗谷'],
    ['2083','遠別商工会','遠別',8,'宗谷'],['2084','天塩商工会','天塩',8,'宗谷'],
    ['2085','幌延町商工会','幌延町',8,'宗谷'],['2086','猿払村商工会','猿払村',8,'宗谷'],
    ['2087','浜頓別町商工会','浜頓別町',9,'オホーツク'],['2088','中頓別町商工会','中頓別町',9,'オホーツク'],
    ['2089','枝幸町商工会','枝幸町',9,'オホーツク'],['2090','豊富町商工会','豊富町',9,'オホーツク'],
    ['2091','礼文町商工会','礼文町',9,'オホーツク'],['2092','利尻町商工会','利尻町',9,'オホーツク'],
    ['2093','利尻富士町商工会','利尻富士町',9,'オホーツク'],['2094','きたみ市商工会','きたみ市',9,'オホーツク'],
    ['2095','津別町商工会','津別町',9,'オホーツク'],['2096','斜里町商工会','斜里町',9,'オホーツク'],
    ['2097','清里町商工会','清里町',9,'オホーツク'],
    ['2098','小清水町商工会','小清水町',10,'十勝'],['2099','訓子府町商工会','訓子府町',10,'十勝'],
    ['2100','置戸町商工会','置戸町',10,'十勝'],['2101','佐呂間町商工会','佐呂間町',10,'十勝'],
    ['2102','えんがる商工会','えんがる',10,'十勝'],['2103','湧別町商工会','湧別町',10,'十勝'],
    ['2104','滝上町商工会','滝上町',10,'十勝'],['2105','興部町商工会','興部町',10,'十勝'],
    ['2106','西興部村商工会','西興部村',10,'十勝'],['2107','雄武町商工会','雄武町',10,'十勝'],
    ['2108','大空町商工会','大空町',10,'十勝'],
    ['2109','豊浦町商工会','豊浦町',11,'釧路'],['2110','壮瞥町商工会','壮瞥町',11,'釧路'],
    ['2111','白老町商工会','白老町',11,'釧路'],['2112','厚真町商工会','厚真町',11,'釧路'],
    ['2113','洞爺湖町商工会','洞爺湖町',11,'釧路'],['2114','安平町商工会','安平町',11,'釧路'],
    ['2115','むかわ町商工会','むかわ町',11,'釧路'],['2116','日高町商工会','日高町',11,'釧路'],
    ['2117','平取町商工会','平取町',11,'釧路'],['2118','新冠町商工会','新冠町',11,'釧路'],
    ['2119','様似町商工会','様似町',11,'釧路'],
    ['2120','えりも町商工会','えりも町',12,'根室'],['2121','新ひだか町商工会','新ひだか町',12,'根室'],
    ['2122','音更町商工会','音更町',12,'根室'],['2123','士幌町商工会','士幌町',12,'根室'],
    ['2124','上士幌町商工会','上士幌町',12,'根室'],['2125','鹿追町商工会','鹿追町',12,'根室'],
    ['2126','新得町商工会','新得町',12,'根室'],['2127','清水町商工会','清水町',12,'根室'],
    ['2128','芽室町商工会','芽室町',12,'根室'],['2129','中札内村商工会','中札内村',12,'根室'],
    ['2130','更別村商工会','更別村',12,'根室'],
    ['2131','大樹町商工会','大樹町',13,'胆振'],['2132','広尾町商工会','広尾町',13,'胆振'],
    ['2133','幕別町商工会','幕別町',13,'胆振'],['2134','池田町商工会','池田町',13,'胆振'],
    ['2135','豊頃町商工会','豊頃町',13,'胆振'],['2136','本別町商工会','本別町',13,'胆振'],
    ['2137','足寄町商工会','足寄町',13,'胆振'],['2138','陸別町商工会','陸別町',13,'胆振'],
    ['2139','浦幌町商工会','浦幌町',13,'胆振'],['2140','釧路町商工会','釧路町',13,'胆振'],
    ['2141','厚岸町商工会','厚岸町',13,'胆振'],
    ['2142','浜中町商工会','浜中町',14,'日高'],['2143','標茶町商工会','標茶町',14,'日高'],
    ['2144','弟子屈町商工会','弟子屈町',14,'日高'],['2145','阿寒町商工会','阿寒町',14,'日高'],
    ['2146','鶴居村商工会','鶴居村',14,'日高'],['2147','白糠町商工会','白糠町',14,'日高'],
    ['2148','音別町商工会','音別町',14,'日高'],['2149','別海町商工会','別海町',14,'日高'],
    ['2150','中標津町商工会','中標津町',14,'日高'],['2151','標津町商工会','標津町',14,'日高'],
    ['2152','羅臼町商工会','羅臼町',14,'日高'],
  ];
  const SHOKOKAI_LIST = SHOKOKAI_ROWS.map(([cd, name, short, gcode, glabel], i) => ({
    cd, name, short, group_code: gcode, group_label: glabel,
    tier: tierForIndex(i, name.length),
  }));

  SHOKOKAI_LIST.unshift({
    cd: '0021', name: '北海道商工会連合会', short: '道連',
    group_code: null, group_label: null, tier: 'h3',
  });

  const REGION_LABELS = { hokkaido: '北海道', tohoku: '東北', kanto: '関東', chubu: '中部', kinki: '近畿', chugoku: '中国', shikoku: '四国', kyushu: '九州・沖縄' };
  const NATIONAL_ROWS = [
    ['01','北海道','北海道','hokkaido'],['02','青森県','青森','tohoku'],['03','岩手県','岩手','tohoku'],
    ['04','宮城県','宮城','tohoku'],['05','秋田県','秋田','tohoku'],['06','山形県','山形','tohoku'],
    ['07','福島県','福島','tohoku'],['08','茨城県','茨城','kanto'],['09','栃木県','栃木','kanto'],
    ['10','群馬県','群馬','kanto'],['11','埼玉県','埼玉','kanto'],['12','千葉県','千葉','kanto'],
    ['13','東京都','東京','kanto'],['14','神奈川県','神奈川','kanto'],['15','新潟県','新潟','chubu'],
    ['16','富山県','富山','chubu'],['17','石川県','石川','chubu'],['18','福井県','福井','chubu'],
    ['19','山梨県','山梨','chubu'],['20','長野県','長野','chubu'],['21','岐阜県','岐阜','chubu'],
    ['22','静岡県','静岡','chubu'],['23','愛知県','愛知','chubu'],['24','三重県','三重','kinki'],
    ['25','滋賀県','滋賀','kinki'],['26','京都府','京都','kinki'],['27','大阪府','大阪','kinki'],
    ['28','兵庫県','兵庫','kinki'],['29','奈良県','奈良','kinki'],['30','和歌山県','和歌山','kinki'],
    ['31','鳥取県','鳥取','chugoku'],['32','島根県','島根','chugoku'],['33','岡山県','岡山','chugoku'],
    ['34','広島県','広島','chugoku'],['35','山口県','山口','chugoku'],['36','徳島県','徳島','shikoku'],
    ['37','香川県','香川','shikoku'],['38','愛媛県','愛媛','shikoku'],['39','高知県','高知','shikoku'],
    ['40','福岡県','福岡','kyushu'],['41','佐賀県','佐賀','kyushu'],['42','長崎県','長崎','kyushu'],
    ['43','熊本県','熊本','kyushu'],['44','大分県','大分','kyushu'],['45','宮崎県','宮崎','kyushu'],
    ['46','鹿児島県','鹿児島','kyushu'],['47','沖縄県','沖縄','kyushu'],
  ];

  const NATIONAL_LIST = NATIONAL_ROWS.map(([cd, prefName, short, region], i) => ({
    cd, name: prefName + '商工会連合会', short, group_code: region, group_label: REGION_LABELS[region],
    tier: tierForIndex(i, prefName.length),
  }));

  const NATIONAL_THEMES = THEMES.map(t => ({ ...t, count: t.count * 42 }));

  const MONTH_LABELS = ['5月', '6月', '7月', '8月'];

  const TIER_BASE = { h5: 34, h4: 22, h3: 14, h2: 8, h1: 4 };

  function buildMonthlyStats(list, scale) {
    return list.map((s, i) => {
      const base = (TIER_BASE[s.tier] || 6) * scale;
      const ytd = Math.max(4, Math.round(base * 4) - i);

      const jitter = [(i * 7) % 11, (i * 13) % 11, (i * 17) % 11, (i * 19) % 11];
      const weights = [0.85, 1.0, 1.05, 1.1].map((w, idx) => w + jitter[idx] * 0.012);
      const weightSum = weights.reduce((a, b) => a + b, 0);
      const counts = weights.map(w => Math.max(1, Math.round(ytd * w / weightSum)));
      const countsSum = counts.reduce((a, b) => a + b, 0);
      counts[3] = Math.max(1, counts[3] + (ytd - countsSum));
      const prior = Math.max(ytd + 1, ytd + 25 + (i * 3) % 97);
      const progress = Math.round((ytd / prior) * 1000) / 10;

      const aiRatio = 0.15 + ((i * 5) % 11) * 0.01;
      const aiCounts = counts.map(c => Math.max(0, Math.round(c * aiRatio)));
      return { name: s.name, counts, progress, prior, aiCounts };
    });
  }

  let CURRENT_LIST = SHOKOKAI_LIST;
  let CURRENT_THEMES = THEMES;
  let CURRENT_MONTHLY_STATS = buildMonthlyStats(SHOKOKAI_LIST, 1);
  let CURRENT_HEATMAP_TITLE = '北海道 支援状況';
  let CURRENT_ALL_LABEL = '全商工会';
  let CURRENT_SELF_LABEL = '県連';
  let CURRENT_TOTAL_LABEL = '北海道 合計';
  let CURRENT_COL_LABEL = '商工会';

  let CURRENT_SHOW_AI = false;
  const excludedShokokai = new Set();

  function themeChartHtml() {

    const sortedThemes = CURRENT_THEMES.slice().sort((a, b) => b.count - a.count);
    const max = Math.max(...sortedThemes.map(t => t.count), 1);
    const bars = sortedThemes.map(t => {
      const height = Math.round((t.count / max) * 90);
      return `
        <div class="bar-wrap">
          <div class="bar-track">
            <div class="bar-val">${t.count.toLocaleString()}</div>
            <div class="bar bar--${t.code}" style="height:${height}px"></div>
          </div>
          <div class="bar-label">${esc(t.label)}</div>
        </div>`;
    }).join('');

    return `
      <div id="dash-theme-chart">
        <div class="card">
          <div class="card-header"><div class="card-title" style="color:var(--text);">支援テーマ別 件数（年度累計）</div></div>
          <div class="card-body"><div class="bar-chart">${bars}</div></div>
        </div>
      </div>
    `;
  }

  const heatmapState = { page: 1, pageSize: 60, totalPages: 1 };
  let heatmapGridEl = null;
  let heatmapIndicatorEl = null;
  let heatmapPageButtons = null;

  function heatmapHtml() {
    const groups = new Map();

    CURRENT_LIST.forEach(s => { if (s.group_code != null && !groups.has(s.group_code)) groups.set(s.group_code, s.group_label); });

    const hasSelfRow = CURRENT_LIST.some(s => s.group_code == null);
    const filterHtml = `
      <label class="pref-filter__all"><input type="checkbox" id="dash-filter-all" checked> ${esc(CURRENT_ALL_LABEL)}</label>
      <span class="pref-filter__sep"></span>
      ${hasSelfRow ? `<label><input type="checkbox" checked data-group-value="__self__"> ${esc(CURRENT_SELF_LABEL)}</label>` : ''}
      ${Array.from(groups.entries()).map(([code, label]) => `<label><input type="checkbox" checked data-group-value="${esc(code)}"> ${esc(label)}</label>`).join('')}
    `;
    return `
      <div class="card" id="dash-heatmap-card">
        <div class="card-header">
          <div class="flex items-center gap-md">

            <div class="card-title">${esc(CURRENT_HEATMAP_TITLE)}</div>
            <div class="grid-pager" id="dash-heatmap-pager">
              <button type="button" class="btn btn-outline btn-sm" style="width:38px;height:19px;padding:0;justify-content:center;" data-page-delta="-1">‹</button>
              <span class="page-indicator" id="dash-heatmap-page-indicator"></span>
              <button type="button" class="btn btn-outline btn-sm" style="width:38px;height:19px;padding:0;justify-content:center;" data-page-delta="1">›</button>
            </div>
          </div>

          <div class="legend">
            <span class="legend-label">低</span>
            <span class="legend-swatch legend-swatch--h1"></span>
            <span class="legend-swatch legend-swatch--h2"></span>
            <span class="legend-swatch legend-swatch--h3"></span>
            <span class="legend-swatch legend-swatch--h4"></span>
            <span class="legend-swatch legend-swatch--h5"></span>
            <span class="legend-label">高</span>
          </div>
        </div>
        <div class="card-body" style="padding:var(--space-5)">
          <div class="pref-filter" id="dash-heatmap-filter">${filterHtml}</div>
          <div class="pref-grid" id="dash-heatmap-grid"></div>
        </div>
      </div>
    `;
  }

  function renderHeatmapPage() {
    if (!heatmapGridEl) return;
    heatmapState.totalPages = Math.max(1, Math.ceil(CURRENT_LIST.length / heatmapState.pageSize));
    const start = (heatmapState.page - 1) * heatmapState.pageSize;
    const pageCells = CURRENT_LIST.slice(start, start + heatmapState.pageSize);
    heatmapGridEl.innerHTML = pageCells.map(s => {
      const isOff = excludedShokokai.has(s.name);
      const groupValue = s.group_code == null ? '__self__' : s.group_code;
      return `<div class="pref-cell ${s.tier}${isOff ? ' is-off' : ''}" data-name="${esc(s.name)}" data-group-value="${esc(groupValue)}" title="${esc(s.name)}">${esc(s.short)}</div>`;
    }).join('');
    if (heatmapIndicatorEl) heatmapIndicatorEl.textContent = heatmapState.page + ' / ' + heatmapState.totalPages;
    if (heatmapPageButtons) heatmapPageButtons.forEach(btn => {
      const delta = parseInt(btn.getAttribute('data-page-delta'), 10);
      btn.disabled = (delta < 0 && heatmapState.page <= 1) || (delta > 0 && heatmapState.page >= heatmapState.totalPages);
    });
    const pagerEl = root.querySelector('#dash-heatmap-pager');
    if (pagerEl) pagerEl.classList.toggle('is-active', heatmapState.totalPages > 1);
  }

  function wireHeatmap() {
    heatmapState.page = 1;
    heatmapGridEl = root.querySelector('#dash-heatmap-grid');
    heatmapIndicatorEl = root.querySelector('#dash-heatmap-page-indicator');
    heatmapPageButtons = root.querySelectorAll('[data-page-delta]');
    const filterEl = root.querySelector('#dash-heatmap-filter');
    if (!heatmapGridEl || !filterEl) return;

    renderHeatmapPage();

    heatmapPageButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const delta = parseInt(btn.getAttribute('data-page-delta'), 10);
        heatmapState.page = Math.min(heatmapState.totalPages, Math.max(1, heatmapState.page + delta));
        renderHeatmapPage();
      });
    });

    heatmapGridEl.addEventListener('click', (e) => {
      const cell = e.target.closest('.pref-cell');
      if (!cell) return;
      const name = cell.getAttribute('data-name');
      if (excludedShokokai.has(name)) excludedShokokai.delete(name); else excludedShokokai.add(name);
      cell.classList.toggle('is-off', excludedShokokai.has(name));
      root.querySelector('#dash-bottom-table').innerHTML = monthlyTableHtml();
    });
    const allCheckbox = filterEl.querySelector('#dash-filter-all');
    const groupBoxes = () => filterEl.querySelectorAll('[data-group-value]');

    const keysForGroup = (value) => value === '__self__'
      ? CURRENT_LIST.filter(s => s.group_code == null).map(s => s.name)
      : CURRENT_LIST.filter(s => String(s.group_code) === String(value)).map(s => s.name);
    groupBoxes().forEach(cb => {
      cb.addEventListener('change', () => {
        keysForGroup(cb.getAttribute('data-group-value')).forEach(name => {
          if (cb.checked) excludedShokokai.delete(name); else excludedShokokai.add(name);
        });
        allCheckbox.checked = Array.from(groupBoxes()).every(b => b.checked);
        renderHeatmapPage();
        root.querySelector('#dash-bottom-table').innerHTML = monthlyTableHtml();
      });
    });
    allCheckbox.addEventListener('change', () => {
      const on = allCheckbox.checked;
      groupBoxes().forEach(cb => { cb.checked = on; });
      if (on) excludedShokokai.clear();
      else CURRENT_LIST.forEach(s => excludedShokokai.add(s.name));
      renderHeatmapPage();
      root.querySelector('#dash-bottom-table').innerHTML = monthlyTableHtml();
    });
  }

  function monthlyTableHtml() {
    const totalCounts = MONTH_LABELS.map((_, i) => CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + r.counts[i], 0));
    const totalYtd = CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + r.counts.reduce((a, b) => a + b, 0), 0);

    const totalAi = CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + (r.aiCounts || []).reduce((a, b) => a + b, 0), 0);
    const rowHtml = (label, counts, ytd, progress, prior, aiYtd, isTotal, hidden) => `
      <tr${isTotal ? ' class="total"' : ''}${hidden ? ' style="display:none"' : ''}>
        <td>${isTotal ? `<strong>${esc(label)}</strong>` : esc(label)}</td>
        ${counts.map(c => `<td class="num">${isTotal ? `<strong>${c.toLocaleString()}</strong>` : c.toLocaleString()}</td>`).join('')}
        <td class="num">${isTotal ? `<strong>${ytd.toLocaleString()}</strong>` : ytd.toLocaleString()}</td>
        <td>
          <div class="flex items-center gap-sm">
            <div class="progress" style="width:120px;flex-shrink:0"><div class="progress__fill ${progress >= 50 ? 'progress__fill--green' : 'progress__fill--accent'}" style="width:${progress}%"></div></div>
            ${progress.toFixed(1)}%（前年度${prior.toLocaleString()}件）
          </div>
        </td>
        ${CURRENT_SHOW_AI ? `<td class="num">${isTotal ? `<strong>${aiYtd.toLocaleString()}</strong>` : aiYtd.toLocaleString()}</td>` : ''}
      </tr>`;

    const sortedStats = CURRENT_MONTHLY_STATS;
    const rows = sortedStats.map(r => rowHtml(
      r.name, r.counts, r.counts.reduce((a, b) => a + b, 0), r.progress, r.prior,
      (r.aiCounts || []).reduce((a, b) => a + b, 0), false, excludedShokokai.has(r.name)
    )).join('');
    const totalRow = rowHtml(CURRENT_TOTAL_LABEL, totalCounts, totalYtd, 58.4, 480, totalAi, true, false);
    return `
      <div class="card card--fill" id="dash-monthly-table-card">
        <div class="card-header" style="background:var(--gold-bg); border-bottom-color:var(--gold-border);"><div class="card-title">${esc(CURRENT_COL_LABEL)}別 月次実績推移（直近4か月）</div></div>
        <div class="table-scroll" id="dash-monthly-table-scroll">
          <table>
            <thead><tr><th>${esc(CURRENT_COL_LABEL)}</th>${MONTH_LABELS.map(m => `<th class="num">${esc(m)}</th>`).join('')}<th class="num">年度累計</th><th>対前年進捗率</th>${CURRENT_SHOW_AI ? '<th class="num">AI活用件数</th>' : ''}</tr></thead>
            <tbody>${totalRow}${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  function render(role) {

    if (role === 'national') {
      CURRENT_LIST = NATIONAL_LIST;
      CURRENT_THEMES = NATIONAL_THEMES;
      CURRENT_MONTHLY_STATS = buildMonthlyStats(NATIONAL_LIST, 8);
      CURRENT_HEATMAP_TITLE = '全国 支援状況';
      CURRENT_ALL_LABEL = '全都道府県';
      CURRENT_SELF_LABEL = '全国連';
      CURRENT_TOTAL_LABEL = '全国 合計';
      CURRENT_COL_LABEL = '都道府県';
      CURRENT_SHOW_AI = true;
    } else {
      CURRENT_LIST = SHOKOKAI_LIST;
      CURRENT_THEMES = THEMES;
      CURRENT_MONTHLY_STATS = buildMonthlyStats(SHOKOKAI_LIST, 1);
      CURRENT_HEATMAP_TITLE = '北海道 支援状況';
      CURRENT_ALL_LABEL = '全商工会';
      CURRENT_SELF_LABEL = '県連';
      CURRENT_TOTAL_LABEL = '北海道 合計';
      CURRENT_COL_LABEL = '商工会';
      CURRENT_SHOW_AI = false;
    }
    excludedShokokai.clear();

    const thisMonthSupport = CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + r.counts[3], 0);
    const priorMonthSupport = CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + r.counts[2], 0);
    const monthDiff = thisMonthSupport - priorMonthSupport;
    const monthChangeLabel = monthDiff === 0 ? '－'
      : (monthDiff > 0 ? '▲' : '▼') + `前月比 ${monthDiff > 0 ? '+' : ''}${monthDiff.toLocaleString()}件`;

    const thisMonthAi = CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + ((r.aiCounts || [])[3] || 0), 0);
    const priorMonthAi = CURRENT_MONTHLY_STATS.reduce((sum, r) => sum + ((r.aiCounts || [])[2] || 0), 0);
    const aiMonthDiff = thisMonthAi - priorMonthAi;
    const aiMonthChangeLabel = aiMonthDiff === 0 ? '－'
      : (aiMonthDiff > 0 ? '▲' : '▼') + `前月比 ${aiMonthDiff > 0 ? '+' : ''}${aiMonthDiff.toLocaleString()}件`;
    const aiStatHtml = role === 'national' ? `
            <span style="border-left:1px solid var(--gold-border); margin:0 var(--space-5); align-self:stretch;"></span>
            <div class="notice-stat__main" style="font-size:var(--fs-sm);">AI活用件数<span class="value" style="font-size:var(--fs-lg);">${thisMonthAi.toLocaleString()}件</span><span class="notice-stat__change">${aiMonthChangeLabel}</span></div>` : '';
    root.innerHTML = `

      <div class="cat-lbl">📢 お知らせ</div>
      <div class="card notice-card" style="margin-bottom:var(--space-8)">
        <div class="notice-panel">

          <div class="kpi-notice-list">
            <div class="notice-item">2026年7月分の月次報告の提出締め切りは2026年8月25日です</div>
            <div class="notice-item"><a href="#reports" class="notice-item-link">下書きのまま保存されている報告書が3件あります</a></div>
          </div>
          <div style="border-left:1px solid var(--gold-border); padding-left:var(--space-7); display:flex; align-items:center;">
            <div class="notice-stat__main">今月の支援件数<span class="value">${thisMonthSupport.toLocaleString()}件</span><span class="notice-stat__change">${monthChangeLabel}</span></div>${aiStatHtml}
          </div>
        </div>
      </div>
      <div class="grid grid-2 grid-gap-md" style="margin-bottom:var(--space-8)">
        ${themeChartHtml()}
        ${heatmapHtml()}
      </div>

      <div id="dash-bottom-table">${monthlyTableHtml()}</div>
    `;

    wireHeatmap();

    requestAnimationFrame(() => {
      const themeHeaderEl = root.querySelector('#dash-theme-chart .card-header');
      const heatmapHeaderEl = root.querySelector('#dash-heatmap-card .card-header');
      if (themeHeaderEl) themeHeaderEl.style.minHeight = '';
      if (heatmapHeaderEl) heatmapHeaderEl.style.minHeight = '';
    });
  }

  window.__renderHomeForRole = (role) => {
    const isFederation = role === 'national' || role === 'pref';
    const shokokaiEl = document.getElementById('home-shokokai-content');
    if (shokokaiEl) shokokaiEl.style.display = isFederation ? 'none' : '';
    root.style.display = isFederation ? '' : 'none';
    if (isFederation) render(role);
  };
  window.__renderHomeForRole(document.getElementById('org-role-select') ? document.getElementById('org-role-select').value : 'pref');
})();
