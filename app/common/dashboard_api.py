"""Dashboard KPI / heatmap helpers (DashboardInit + heatmap APIs)."""
import json
import utils.mysqldb_utils as db
from app.common.api_json import jsonable_row, jsonable_rows
import utils.string_util

REGION_LABELS = {
    "hokkaido": "北海道",
    "tohoku": "東北",
    "kanto": "関東",
    "chubu": "中部",
    "kinki": "近畿",
    "chugoku": "中国",
    "shikoku": "四国",
    "kyushu": "九州・沖縄",
}

FE_ROLE_TO_NOTICE = {
    "national": "zenkoku",
    "pref": "ken",
    "shokokai": "shokokai",
}


def _q(sql, params=None):
    return db.result_to_list_of_dict(db.querySQL(sql, params or {})) or []


def org_from_session(session, dto=None):
    """Resolve org. Client org is trusted only when BOTH codes are present;
    otherwise use the login session pair (avoids localStorage pref-only → 00/0021 misses)."""
    pref = ""
    shokokai = ""
    if dto is not None:
        pref = utils.string_util.changeNullToBlank(getattr(dto, "prefecturecode", ""))
        shokokai = utils.string_util.changeNullToBlank(getattr(dto, "shokokaicd", ""))
    if not pref or not shokokai:
        pref = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
        shokokai = utils.string_util.changeNullToBlank(session.get("SHOKOKAI_CD"))
    return pref, shokokai


def latest_fiscal_year_id(prefecture_code, shokokai_cd):
    rows = _q(
        """
SELECT fiscal_year_id
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND deleted_at IS NULL
ORDER BY fiscal_year_id DESC
LIMIT 1
""",
        {"prefecture_code": prefecture_code, "shokokai_cd": shokokai_cd},
    )
    if not rows:
        return ""
    return str(rows[0].get("fiscal_year_id") or "")


def fetch_kpi(prefecture_code, shokokai_cd, fiscal_year_id):
    params = {
        "prefecture_code": prefecture_code,
        "shokokai_cd": shokokai_cd,
        "fiscal_year_id": fiscal_year_id,
    }
    sql = """
SELECT COALESCE(SUM(support_count), 0) AS support_count,
       COALESCE(SUM(ai_activity_count), 0) AS ai_activity_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_prefecture_code IS NULL
  AND target_shokokai_cd IS NULL
  AND deleted_at IS NULL
"""
    if fiscal_year_id not in (None, ""):
        sql += "  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)\n"
    else:
        params.pop("fiscal_year_id", None)
    rows = _q(sql, params)
    rec = rows[0] if rows else {}
    return int(rec.get("support_count") or 0), int(rec.get("ai_activity_count") or 0)


def fetch_themes(prefecture_code, shokokai_cd, fiscal_year_id):
    params = {
        "prefecture_code": prefecture_code,
        "shokokai_cd": shokokai_cd,
    }
    sql = """
SELECT t.theme_code,
       t.label,
       t.badge_class,
       SUM(b.support_count) AS support_count
FROM trn_kpi_theme_breakdown b
JOIN mst_theme t ON t.theme_id = b.theme_id
WHERE b.prefecture_code = :prefecture_code
  AND b.shokokai_cd = :shokokai_cd
  AND b.deleted_at IS NULL
"""
    if fiscal_year_id not in (None, ""):
        sql += "  AND b.fiscal_year_id = CAST(:fiscal_year_id AS integer)\n"
        params["fiscal_year_id"] = fiscal_year_id
    sql += """
GROUP BY t.theme_code, t.label, t.badge_class, t.group_order
ORDER BY SUM(b.support_count) DESC, t.group_order
"""
    out = []
    for rec in _q(sql, params):
        out.append(
            {
                "code": str(rec.get("theme_code") or ""),
                "label": str(rec.get("label") or ""),
                "count": int(rec.get("support_count") or 0),
                "badge_class": str(rec.get("badge_class") or ""),
            }
        )
    return out


def _tier_for_count(count, min_c, max_c):
    if max_c <= min_c:
        return "h3"
    ratio = (count - min_c) / float(max_c - min_c)
    if ratio >= 0.8:
        return "h5"
    if ratio >= 0.6:
        return "h4"
    if ratio >= 0.4:
        return "h3"
    if ratio >= 0.2:
        return "h2"
    return "h1"


def fetch_heatmap_cells(fe_role, prefecture_code, shokokai_cd, fiscal_year_id):
    cells = []
    if fe_role == "national":
        rows = _q(
            """
SELECT p.prefecture_code AS cd,
       p.name AS name,
       p.short_name AS short,
       p.region AS group_code,
       COALESCE(SUM(d.support_count), 0) AS ytd
FROM mst_prefecture p
LEFT JOIN trn_kpi_monthly_stat d
  ON d.target_prefecture_code = p.prefecture_code
 AND d.prefecture_code = :prefecture_code
 AND d.shokokai_cd = :shokokai_cd
 AND d.target_shokokai_cd IS NULL
 AND d.deleted_at IS NULL
 AND d.fiscal_year_id = CAST(:fiscal_year_id AS integer)
WHERE p.deleted_at IS NULL
  AND p.prefecture_code <> '00'
GROUP BY p.prefecture_code, p.name, p.short_name, p.region, p.sort_order
ORDER BY p.sort_order
""",
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "fiscal_year_id": fiscal_year_id,
            },
        )
        for rec in rows:
            gcode = str(rec.get("group_code") or "")
            cells.append(
                {
                    "cd": str(rec.get("cd") or ""),
                    "name": str(rec.get("name") or "") + "商工会連合会",
                    "short": str(rec.get("short") or ""),
                    "group_code": gcode,
                    "group_label": REGION_LABELS.get(gcode, gcode),
                    "ytd": int(rec.get("ytd") or 0),
                    "cell_key": str(rec.get("name") or "") + "商工会連合会",
                }
            )
    else:
        fed = _q(
            """
SELECT shokokai_cd, name, short_name
FROM mst_shokokai
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND deleted_at IS NULL
LIMIT 1
""",
            {"prefecture_code": prefecture_code, "shokokai_cd": shokokai_cd},
        )
        if fed:
            f = fed[0]
            ytd_rows = _q(
                """
SELECT COALESCE(SUM(support_count), 0) AS ytd
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_prefecture_code IS NULL
  AND target_shokokai_cd IS NULL
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
  AND deleted_at IS NULL
""",
                {
                    "prefecture_code": prefecture_code,
                    "shokokai_cd": shokokai_cd,
                    "fiscal_year_id": fiscal_year_id,
                },
            )
            ytd = int((ytd_rows[0] if ytd_rows else {}).get("ytd") or 0)
            cells.append(
                {
                    "cd": str(f.get("shokokai_cd") or shokokai_cd),
                    "name": str(f.get("name") or ""),
                    "short": str(f.get("short_name") or f.get("name") or ""),
                    "group_code": None,
                    "group_label": None,
                    "ytd": ytd,
                    "cell_key": str(f.get("name") or shokokai_cd),
                }
            )
        rows = _q(
            """
SELECT s.shokokai_cd AS cd,
       s.name AS name,
       s.short_name AS short,
       CAST(s.group_code AS text) AS group_code,
       s.group_label,
       COALESCE(SUM(d.support_count), 0) AS ytd
FROM mst_shokokai s
LEFT JOIN trn_kpi_monthly_stat d
  ON d.target_shokokai_cd = s.shokokai_cd
 AND d.prefecture_code = :prefecture_code
 AND d.shokokai_cd = :shokokai_cd
 AND d.target_prefecture_code IS NULL
 AND d.fiscal_year_id = CAST(:fiscal_year_id AS integer)
 AND d.deleted_at IS NULL
WHERE s.prefecture_code = :prefecture_code
  AND s.shokokai_cd <> :shokokai_cd
  AND s.deleted_at IS NULL
GROUP BY s.shokokai_cd, s.name, s.short_name, s.group_code, s.group_label, s.sort_order
ORDER BY s.sort_order, s.shokokai_cd
""",
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "fiscal_year_id": fiscal_year_id,
            },
        )
        for rec in rows:
            cells.append(
                {
                    "cd": str(rec.get("cd") or ""),
                    "name": str(rec.get("name") or ""),
                    "short": str(rec.get("short") or rec.get("name") or ""),
                    "group_code": rec.get("group_code"),
                    "group_label": rec.get("group_label"),
                    "ytd": int(rec.get("ytd") or 0),
                    "cell_key": str(rec.get("name") or rec.get("cd") or ""),
                }
            )

    counts = [c["ytd"] for c in cells]
    min_c = min(counts) if counts else 0
    max_c = max(counts) if counts else 0
    for c in cells:
        c["tier"] = _tier_for_count(c["ytd"], min_c, max_c)
    return cells


def month_labels(prefecture_code, shokokai_cd, fiscal_year_id, limit=4):
    rows = _q(
        """
SELECT DISTINCT year_month
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
  AND deleted_at IS NULL
ORDER BY year_month DESC
LIMIT :lim
""",
        {
            "prefecture_code": prefecture_code,
            "shokokai_cd": shokokai_cd,
            "fiscal_year_id": fiscal_year_id,
            "lim": limit,
        },
    )
    months = list(reversed([r["year_month"] for r in rows if r.get("year_month")]))
    labels = []
    for ym in months:
        part = str(ym).split("-")
        labels.append(part[1].lstrip("0") + "月" if len(part) == 2 else str(ym))
    return months, labels


def fetch_monthly_stats(fe_role, prefecture_code, shokokai_cd, fiscal_year_id, cells, year_months):
    if not year_months:
        return []
    ym_params = {f"m{i}": ym for i, ym in enumerate(year_months)}
    ym_in = ", ".join(f":m{i}" for i in range(len(year_months)))
    stats = []
    for cell in cells:
        params = {
            "prefecture_code": prefecture_code,
            "shokokai_cd": shokokai_cd,
            "fiscal_year_id": fiscal_year_id,
            **ym_params,
        }
        if fe_role == "national":
            sql = f"""
SELECT year_month, SUM(support_count) AS support_count,
       SUM(COALESCE(ai_activity_count, 0)) AS ai_activity_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_prefecture_code = :target_key
  AND target_shokokai_cd IS NULL
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
  AND year_month IN ({ym_in})
  AND deleted_at IS NULL
GROUP BY year_month
"""
            params["target_key"] = cell.get("cd") or ""
        else:
            if cell.get("group_code") is None:
                sql = f"""
SELECT year_month, SUM(support_count) AS support_count,
       SUM(COALESCE(ai_activity_count, 0)) AS ai_activity_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_prefecture_code IS NULL
  AND target_shokokai_cd IS NULL
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
  AND year_month IN ({ym_in})
  AND deleted_at IS NULL
GROUP BY year_month
"""
            else:
                sql = f"""
SELECT year_month, SUM(support_count) AS support_count,
       SUM(COALESCE(ai_activity_count, 0)) AS ai_activity_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_shokokai_cd = :target_key
  AND target_prefecture_code IS NULL
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
  AND year_month IN ({ym_in})
  AND deleted_at IS NULL
GROUP BY year_month
"""
                params["target_key"] = cell.get("cd") or ""

        by_month = {r["year_month"]: r for r in _q(sql, params)}
        counts = [int((by_month.get(ym) or {}).get("support_count") or 0) for ym in year_months]
        ai_counts = [int((by_month.get(ym) or {}).get("ai_activity_count") or 0) for ym in year_months]
        ytd = sum(counts)
        prior_rows = _q(
            """
SELECT COALESCE(SUM(support_count), 0) AS prior
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND fiscal_year_id = CAST(:prior_fy AS integer)
  AND deleted_at IS NULL
  AND (
    (CAST(:fiscal_year_id AS integer) > 0 AND fiscal_year_id = CAST(:prior_fy AS integer))
  )
""",
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "fiscal_year_id": fiscal_year_id,
                "prior_fy": str(max(1, int(fiscal_year_id or 1) - 1)),
            },
        )
        prior = int((prior_rows[0] if prior_rows else {}).get("prior") or max(ytd + 1, 1))
        progress = round((ytd / prior) * 1000) / 10 if prior else 0.0
        stats.append(
            {
                "name": cell.get("name") or "",
                "cell_key": cell.get("cell_key") or cell.get("name") or "",
                "counts": counts,
                "ai_counts": ai_counts,
                "progress": progress,
                "prior": prior,
            }
        )
    return stats


def fetch_notices(fe_role):
    """互換ラッパ：顧客設計 get_active_notices を呼ぶ。"""
    from app.dashboard.services import ensure_notice_dates, get_active_notices

    ensure_notice_dates()
    rc = FE_ROLE_TO_NOTICE.get(fe_role, "ken")
    return get_active_notices(rc)


def parse_excluded_keys(raw):
    if raw in (None, ""):
        return set()
    if isinstance(raw, list):
        return set(str(x) for x in raw if str(x).strip())
    text = str(raw).strip()
    if text.startswith("["):
        try:
            arr = json.loads(text)
            return set(str(x) for x in arr if str(x).strip())
        except Exception:
            pass
    return set(x.strip() for x in text.split("\u001f") if x.strip())


def apply_group_filter(cells, group_values_raw, include_all):
    if include_all in (True, "true", "1", 1, "True"):
        return set()
    groups = set()
    if group_values_raw not in (None, ""):
        for part in str(group_values_raw).split(","):
            part = part.strip()
            if part:
                groups.add(part)
    excluded = set()
    for cell in cells:
        g = cell.get("group_code")
        gkey = "__self__" if g is None else str(g)
        if gkey not in groups:
            excluded.add(cell.get("cell_key") or cell.get("name") or "")
    return excluded


def paginate_cells(cells, page, page_size):
    page = max(1, int(page or 1))
    page_size = max(1, int(page_size or 60))
    total = len(cells)
    total_pages = max(1, (total + page_size - 1) // page_size)
    if page > total_pages:
        page = total_pages
    start = (page - 1) * page_size
    return cells[start : start + page_size], page, total_pages


def fetch_recent_reports(prefecture_code, shokokai_cd, limit=4):
    """互換ラッパ：顧客設計 get_recent_reports を呼ぶ。"""
    from app.dashboard.services import get_recent_reports

    return get_recent_reports(prefecture_code, shokokai_cd, limit)


def build_init_payload(fe_role, prefecture_code, shokokai_cd):
    from datetime import date

    from app.common.menu import get_visible_menu
    from app.common.session import get_current_organization, get_current_user, refresh_session_profile
    from app.dashboard.services import (
        get_current_month_support_count,
        get_kpi_summaries_by_years,
    )
    from app.manual_input.services import count_draft_reports

    fiscal_year_id = latest_fiscal_year_id(prefecture_code, shokokai_cd)
    if not fiscal_year_id:
        fiscal_year_id = "3"

    profile = refresh_session_profile()
    org = profile.get("organization") or get_current_organization()
    user = profile.get("user") or get_current_user()

    notices = fetch_notices(fe_role)
    recent_reports = fetch_recent_reports(prefecture_code, shokokai_cd, 4)
    draft_count = count_draft_reports(prefecture_code, shokokai_cd, fiscal_year_id)
    menus = get_visible_menu(fe_role)

    today = date.today()
    this_ym = today.strftime("%Y-%m")
    if today.month == 1:
        prior_ym = f"{today.year - 1}-12"
    else:
        prior_ym = f"{today.year}-{today.month - 1:02d}"
    # 商工会：ログイン組織のライブ COUNT。県連／全国連は後で monthly_stats 合算に差し替え。
    this_month = get_current_month_support_count(prefecture_code, shokokai_cd, this_ym)
    prior_month = get_current_month_support_count(prefecture_code, shokokai_cd, prior_ym)

    kpi_ai = get_kpi_summaries_by_years(
        prefecture_code, shokokai_cd, [fiscal_year_id]
    )
    ai_count = int(kpi_ai[0]["ai_proposal_count"]) if kpi_ai else 0
    # 年度累計の支援件数は従来 KPI も併用
    support_count, _legacy_ai = fetch_kpi(prefecture_code, shokokai_cd, fiscal_year_id)
    if not ai_count:
        ai_count = int(_legacy_ai or 0)

    common = {
        "rolecode": fe_role,
        "prefecturecode": prefecture_code,
        "shokokaicd": shokokai_cd,
        "fiscalyearid": fiscal_year_id,
        "notices": notices,
        "recent_reports": recent_reports,
        "draftcount": draft_count,
        "menus": menus,
        "orgname": profile.get("orgname") or utils.string_util.changeNullToBlank(org.get("name")),
        "userid": profile.get("userid") or utils.string_util.changeNullToBlank(user.get("user_id")),
        "username": profile.get("username")
        or utils.string_util.changeNullToBlank(user.get("name") or user.get("shokuin_kj")),
        "permissionlevel": profile.get("permissionlevel")
        or utils.string_util.changeNullToBlank(user.get("permission_level")),
        "supportcount": support_count,
        "aiactivitycount": ai_count,
        "thismonthsupport": this_month,
        "priormonthsupport": prior_month,
    }

    # 商工会ホームは直近報告が主。ヒートマップ系は県連／全国連のみ組み立てる。
    if fe_role == "shokokai":
        return {
            **common,
            "themes": [],
            "heatmap": [],
            "monthly_stats": [],
            "month_labels": [],
        }

    themes = fetch_themes(prefecture_code, shokokai_cd, fiscal_year_id)
    cells = fetch_heatmap_cells(fe_role, prefecture_code, shokokai_cd, fiscal_year_id)
    year_months, month_label_list = month_labels(prefecture_code, shokokai_cd, fiscal_year_id)
    monthly_stats = fetch_monthly_stats(
        fe_role, prefecture_code, shokokai_cd, fiscal_year_id, cells, year_months
    )

    # 県連／全国連：お知らせ横の「今月の支援件数」はヒートマップと同口径（月次表の当月／前月合算）
    this_month = 0
    prior_month = 0
    for row in monthly_stats or []:
        counts = row.get("counts") or []
        if counts:
            try:
                this_month += int(counts[-1] or 0)
            except (TypeError, ValueError):
                pass
        if len(counts) > 1:
            try:
                prior_month += int(counts[-2] or 0)
            except (TypeError, ValueError):
                pass
    common["thismonthsupport"] = this_month
    common["priormonthsupport"] = prior_month

    if fe_role == "national":
        meta = {
            "heatmap_title": "全国 支援状況",
            "all_label": "全都道府県",
            "self_label": "全国連",
            "total_label": "全国 合計",
            "col_label": "都道府県",
            "show_ai": True,
        }
    else:
        pref_name = ""
        prow = _q(
            "SELECT name FROM mst_prefecture WHERE prefecture_code = :p LIMIT 1",
            {"p": prefecture_code},
        )
        if prow:
            pref_name = str(prow[0].get("name") or "")
        meta = {
            "heatmap_title": (pref_name or "道") + " 支援状況",
            "all_label": "全商工会",
            "self_label": "県連",
            "total_label": (pref_name or "北海道") + " 合計",
            "col_label": "商工会",
            "show_ai": False,
        }

    return {
        **common,
        "themes": themes,
        "heatmap": cells,
        "monthly_stats": monthly_stats,
        "month_labels": month_label_list,
        "year_months": year_months,
        **meta,
    }


def set_json_success(jsonObj, payload):
    for key, value in payload.items():
        jsonObj.setValue(key, value)
    import utils.json_constant

    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
