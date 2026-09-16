"""報告書を見る: Init / Search / Detail / CSV helpers."""
import json
from datetime import date

from flask import session

import utils.json_constant
import utils.mysqldb_utils as db
import utils.string_util
from app.common.api_json import jsonable_row


def _q(sql, params=None):
    return db.result_to_list_of_dict(db.querySQL(sql, params or {})) or []


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def _g(dto, *names):
    if dto is None:
        return ""
    for name in names:
        val = _blank(getattr(dto, name, ""))
        if val != "":
            return val
    return ""


def _flag(v):
    if v is True:
        return True
    s = str(v or "").strip().lower()
    return s in ("1", "true", "t", "yes", "on", "checked")


def _fmt_date(v):
    if v is None or v == "":
        return ""
    if hasattr(v, "isoformat"):
        return str(v)[:10]
    return str(v)[:10]


def _reiwa_year(gregorian_year):
    try:
        y = int(gregorian_year)
    except (TypeError, ValueError):
        return ""
    n = y - 2018
    return str(n) if n >= 1 else ""


def _month_label(ym):
    parts = str(ym or "").split("-")
    if len(parts) < 2:
        return str(ym or "")
    reiwa = _reiwa_year(parts[0])
    try:
        month = int(parts[1])
    except (TypeError, ValueError):
        return str(ym)
    if reiwa:
        return "　令和%s年%s月" % (reiwa, month)
    return "　%s年%s月" % (parts[0], month)


def iter_months(start_month, end_month):
    try:
        sy, sm = [int(x) for x in str(start_month).split("-")[:2]]
        ey, em = [int(x) for x in str(end_month).split("-")[:2]]
    except (TypeError, ValueError):
        return
    y, m = sy, sm
    while (y, m) <= (ey, em):
        yield "%04d-%02d" % (y, m)
        m += 1
        if m > 12:
            m = 1
            y += 1


def fiscal_years():
    rows = _q(
        """
SELECT fiscal_year_id, fiscal_year_code, label, start_month, end_month
FROM mst_fiscal_year
WHERE deleted_at IS NULL
ORDER BY fiscal_year_code DESC
"""
    )
    out = []
    for rec in rows:
        start_month = _blank(rec.get("start_month"))
        end_month = _blank(rec.get("end_month"))
        months = [{"value": ym, "label": _month_label(ym)} for ym in iter_months(start_month, end_month)]
        out.append(
            {
                "fiscal_year_id": rec.get("fiscal_year_id"),
                "fiscal_year_code": _blank(rec.get("fiscal_year_code")),
                "label": _blank(rec.get("label")),
                "start_month": start_month,
                "end_month": end_month,
                "months": months,
            }
        )
    return out


def prefectures():
    rows = _q(
        """
SELECT prefecture_code, name, short_name, region, sort_order
FROM mst_prefecture
WHERE deleted_at IS NULL
  AND prefecture_code <> '00'
ORDER BY sort_order, prefecture_code
"""
    )
    return [
        {
            "prefecture_code": _blank(rec.get("prefecture_code")),
            "name": _blank(rec.get("name")),
            "short_name": _blank(rec.get("short_name")),
        }
        for rec in rows
    ]


def shokokai_options(prefecture_code=""):
    params = {"prefecture_code": prefecture_code}
    sql = """
SELECT a.prefecture_code, a.shokokai_cd, a.name
FROM mst_shokokai a
JOIN mst_prefecture p ON p.prefecture_code = a.prefecture_code
WHERE a.deleted_at IS NULL
"""
    if prefecture_code:
        sql += "  AND a.prefecture_code = :prefecture_code\n"
    sql += "ORDER BY p.sort_order, a.sort_order, a.shokokai_cd"
    return [
        {
            "prefecture_code": _blank(rec.get("prefecture_code")),
            "shokokai_cd": _blank(rec.get("shokokai_cd")),
            "name": _blank(rec.get("name")),
        }
        for rec in _q(sql, params)
    ]


def report_forms(fiscal_year_id=""):
    params = {}
    sql = """
SELECT form_code, short_label, full_label, badge_class, fiscal_year_id
FROM mst_form
WHERE deleted_at IS NULL
  AND badge_class IS NOT NULL
  AND badge_class <> ''
"""
    if fiscal_year_id not in (None, ""):
        sql += "  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)\n"
        params["fiscal_year_id"] = fiscal_year_id
    sql += """
ORDER BY CASE WHEN form_code = 'F' THEN 0 ELSE 1 END, form_code, fiscal_year_id DESC
"""
    seen = set()
    out = []
    for rec in _q(sql, params):
        code = _blank(rec.get("form_code"))
        if not code or code in seen:
            continue
        seen.add(code)
        out.append(
            {
                "form_code": code,
                "short_label": _blank(rec.get("short_label")),
                "full_label": _blank(rec.get("full_label")),
                "badge_class": _blank(rec.get("badge_class")) or "#1a6fa8",
            }
        )
    return out


def themes():
    rows = _q(
        """
SELECT DISTINCT ON (label) theme_id, theme_code, label, badge_class, group_order
FROM mst_theme
WHERE deleted_at IS NULL
ORDER BY label, group_order, theme_id
"""
    )
    rows.sort(key=lambda r: (int(r.get("group_order") or 0), str(r.get("label") or "")))
    return [
        {
            "theme_id": rec.get("theme_id"),
            "theme_code": _blank(rec.get("theme_code")),
            "label": _blank(rec.get("label")),
            "badge_class": _blank(rec.get("badge_class")),
        }
        for rec in rows
    ]


def resolve_scope(dto):
    role = _g(dto, "rolecode", "role_code") or "shokokai"
    pref_filter = _g(dto, "prefecturecode", "prefecture_code")
    sho_filter = _g(dto, "shokokaicd", "shokokai_cd")
    sess_pref = _blank(session.get("PREFECTURE_CODE"))
    sess_sho = _blank(session.get("SHOKOKAI_CD"))
    # Session org '00' is 全国連 pseudo code; reports live under real prefectures.
    if sess_pref == "00" and role == "shokokai":
        role = "national"
    if pref_filter == "00":
        pref_filter = ""
    role_pref = ""
    role_sho = ""
    if role == "shokokai":
        role_pref = sess_pref
        role_sho = sess_sho
        pref_filter = ""
        sho_filter = ""
    elif role == "pref":
        role_pref = sess_pref or pref_filter
        if role_pref == "00":
            role_pref = ""
        pref_filter = ""
    return {
        "role": role,
        "role_prefecture_code": role_pref,
        "role_shokokai_cd": role_sho,
        "prefecture_code": pref_filter,
        "shokokai_cd": sho_filter,
    }


def _resolve_year_month(dto, years=None):
    year_month = _g(dto, "yearmonth", "year_month")
    fy_start = _g(dto, "fystartmonth", "fy_start_month")
    fy_end = _g(dto, "fyendmonth", "fy_end_month")
    if year_month.startswith("FY:"):
        code = year_month[3:]
        years = years if years is not None else fiscal_years()
        for fy in years:
            if fy.get("fiscal_year_code") == code:
                return "", fy.get("start_month") or "", fy.get("end_month") or ""
        return "", fy_start, fy_end
    return year_month, fy_start, fy_end


def _normalize_form(form):
    form = _blank(form)
    if form in ("", "全様式", "全様式（F・G）"):
        return ""
    return form


def report_row_to_selmap(rec):
    rec = jsonable_row(rec)
    main = _blank(rec.get("staff_main_name"))
    sub = _blank(rec.get("staff_sub_name"))
    staff = main
    if sub:
        staff = main + "／" + sub if main else sub
    summary = _blank(rec.get("summary"))
    content = _blank(rec.get("content_text")) or _blank(rec.get("content")) or summary
    status = _blank(rec.get("status")) or "登録済み"
    printed_at = _fmt_date(rec.get("printed_at"))
    form_code = _blank(rec.get("form_code"))
    return {
        "report_id": rec.get("report_id"),
        "report_code": _blank(rec.get("report_code")),
        "form_code": form_code,
        "form_short_label": _blank(rec.get("form_short_label")) or form_code,
        "form_full_label": _blank(rec.get("form_full_label")),
        "form_badge_class": _blank(rec.get("form_badge_class")) or "#1a6fa8",
        "report_date": _fmt_date(rec.get("report_date")),
        "theme_id": rec.get("theme_id"),
        "theme_code": _blank(rec.get("theme_code")),
        "theme_label": _blank(rec.get("theme_label")),
        "summary": summary,
        "content": content,
        "staff_main_name": main,
        "staff_sub_name": sub,
        "staff_label": staff,
        "prefecture_code": _blank(rec.get("prefecture_code")),
        "shokokai_cd": _blank(rec.get("shokokai_cd")),
        "prefecture_name": _blank(rec.get("prefecture_name")),
        "shokokai_name": _blank(rec.get("shokokai_name")),
        "status": status,
        "printed_at": printed_at,
        "printed": bool(printed_at),
        "time_start": _blank(rec.get("time_start")),
        "time_end": _blank(rec.get("time_end")),
        "business_name": _blank(rec.get("business_name")),
        "business_person": _blank(rec.get("business_person")),
    }


def fetch_reports(dto, years=None):
    scope = resolve_scope(dto)
    year_month, fy_start, fy_end = _resolve_year_month(dto, years)
    form = _normalize_form(_g(dto, "form", "formcode", "form_code"))
    theme = _g(dto, "theme")
    keyword = _g(dto, "keyword")
    include_draft = _flag(_g(dto, "includedraft", "include_draft"))
    unprinted_only = _flag(_g(dto, "unprintedonly", "unprinted_only"))
    params = {
        "role_prefecture_code": scope["role_prefecture_code"],
        "role_shokokai_cd": scope["role_shokokai_cd"],
        "prefecture_code": scope["prefecture_code"],
        "shokokai_cd": scope["shokokai_cd"],
        "year_month": year_month,
        "fy_start_month": fy_start,
        "fy_end_month": fy_end,
        "form": form,
        "theme": theme,
        "keyword": keyword,
    }
    sql = """
SELECT r.report_id
     , r.report_code
     , r.industry_code AS industry
     , r.report_date
     , r.summary
     , COALESCE(NULLIF(r.summary, ''), LEFT(COALESCE(r.content, ''), 80), '') AS content_text
     , r.content
     , r.staff_main_name
     , r.staff_sub_name
     , r.registered_at
     , r.prefecture_code
     , r.shokokai_cd
     , p.name AS prefecture_name
     , s.name AS shokokai_name
     , t.label AS theme_label
     , t.theme_code AS theme_code
     , t.badge_class AS theme_badge_class
     , r.theme_id
     , r.form_code
     , COALESCE(f.short_label, r.form_code, '') AS form_short_label
     , COALESCE(f.full_label, r.form_code, '') AS form_full_label
     , COALESCE(f.badge_class, '#1a6fa8') AS form_badge_class
     , r.status
     , r.printed_at
     , r.time_start
     , r.time_end
     , r.business_name
     , r.business_person
FROM trn_report r
LEFT JOIN mst_prefecture p ON p.prefecture_code = r.prefecture_code
LEFT JOIN mst_shokokai s
  ON s.prefecture_code = r.prefecture_code AND s.shokokai_cd = r.shokokai_cd
LEFT JOIN mst_theme t ON t.theme_id = r.theme_id
LEFT JOIN mst_form f
  ON f.form_code = r.form_code AND f.fiscal_year_id = r.fiscal_year_id
WHERE r.deleted_at IS NULL
  AND COALESCE(r.status, '') <> '削除'
"""
    if params["role_prefecture_code"]:
        sql += "  AND r.prefecture_code = :role_prefecture_code\n"
    if params["role_shokokai_cd"]:
        sql += "  AND r.shokokai_cd = :role_shokokai_cd\n"
    if params["prefecture_code"]:
        sql += "  AND r.prefecture_code = :prefecture_code\n"
    if params["shokokai_cd"]:
        sql += "  AND r.shokokai_cd = :shokokai_cd\n"
    if params["year_month"]:
        sql += "  AND to_char(r.report_date, 'YYYY-MM') = :year_month\n"
    elif params["fy_start_month"] and params["fy_end_month"]:
        sql += "  AND to_char(r.report_date, 'YYYY-MM') BETWEEN :fy_start_month AND :fy_end_month\n"
    if form:
        sql += """  AND (
        (:form = '様式F' AND r.form_code = 'F')
        OR (:form = '全様式G' AND r.form_code IS NOT NULL AND r.form_code <> 'F'
            AND r.form_code NOT LIKE 'H%' AND r.form_code NOT LIKE 'I%')
        OR r.form_code = :form
      )
"""
    if theme:
        sql += "  AND (t.label = :theme OR t.theme_code = :theme OR CAST(r.theme_id AS text) = :theme)\n"
    if keyword:
        sql += """  AND (
        COALESCE(r.summary, '') ILIKE '%' || :keyword || '%'
        OR COALESCE(r.content, '') ILIKE '%' || :keyword || '%'
        OR COALESCE(r.staff_main_name, '') ILIKE '%' || :keyword || '%'
        OR COALESCE(r.staff_sub_name, '') ILIKE '%' || :keyword || '%'
        OR COALESCE(r.business_name, '') ILIKE '%' || :keyword || '%'
      )
"""
    if include_draft:
        sql += "  AND r.status = '下書き'\n"
    if unprinted_only:
        sql += "  AND r.printed_at IS NULL\n"
    sql += "ORDER BY r.report_date DESC NULLS LAST, r.report_id DESC"
    return [report_row_to_selmap(rec) for rec in _q(sql, params)]


def mark_reports_printed(rows):
    """CSV出力対象を印刷済みにする（printed_at 未設定のもののみ）。"""
    ids = []
    for rec in rows or []:
        rid = rec.get("report_id") if isinstance(rec, dict) else None
        if rid is None or rid == "":
            continue
        try:
            ids.append(int(rid))
        except (TypeError, ValueError):
            continue
    # unique preserve order
    seen = set()
    uniq = []
    for i in ids:
        if i in seen:
            continue
        seen.add(i)
        uniq.append(i)
    if not uniq:
        return 0
    account_id = _blank(session.get("USER_ACCOUNT_ID"))
    try:
        updated_by = int(account_id) if account_id else None
    except (TypeError, ValueError):
        updated_by = None
    # chunk to keep statement size bounded
    marked = 0
    chunk_size = 200
    for start in range(0, len(uniq), chunk_size):
        chunk = uniq[start:start + chunk_size]
        params = {"updated_by": updated_by}
        placeholders = []
        for idx, rid in enumerate(chunk):
            key = "rid%d" % idx
            params[key] = rid
            placeholders.append(":" + key)
        sql = (
            "UPDATE trn_report\n"
            "   SET printed_at = CURRENT_DATE\n"
            "     , updated_at = TO_CHAR(NOW(), 'YYYYMMDDHH24MISS')\n"
            "     , updated_by = COALESCE(:updated_by, updated_by)\n"
            " WHERE report_id IN (" + ", ".join(placeholders) + ")\n"
            "   AND deleted_at IS NULL\n"
            "   AND printed_at IS NULL"
        )
        db.updateSQL(sql, params)
        marked += len(chunk)
    return marked


def default_year_month(years):
    if not years:
        today = date.today()
        return "%04d-%02d" % (today.year, today.month)
    fy = years[0]
    code = fy.get("fiscal_year_code") or ""
    if code:
        return "FY:" + code
    today = date.today()
    current = "%04d-%02d" % (today.year, today.month)
    months = [m.get("value") for m in (fy.get("months") or [])]
    if current in months:
        return current
    return months[-1] if months else current


def fetch_report_detail(report_id):
    report_id = _blank(report_id)
    if not report_id:
        return None
    rows = _q(
        """
SELECT r.report_id
     , r.report_code
     , r.form_code
     , r.fiscal_year_id
     , r.prefecture_code
     , r.shokokai_cd
     , r.theme_id
     , r.industry_code AS industry
     , r.report_date
     , r.summary
     , r.content
     , r.time_start
     , r.time_end
     , r.business_person
     , r.business_name
     , r.staff_main_name
     , r.staff_sub_name
     , r.registered_at
     , r.status
     , r.printed_at
     , COALESCE(f.full_label, r.form_code, '') AS form_full_label
     , COALESCE(f.short_label, r.form_code, '') AS form_short_label
     , t.theme_code AS primary_theme_code
     , t.label AS theme_label
FROM trn_report r
LEFT JOIN mst_form f
  ON f.form_code = r.form_code AND f.fiscal_year_id = r.fiscal_year_id
LEFT JOIN mst_theme t ON t.theme_id = r.theme_id
WHERE r.report_id = CAST(:report_id AS integer)
  AND r.deleted_at IS NULL
  AND COALESCE(r.status, '') <> '削除'
""",
        {"report_id": report_id},
    )
    if not rows:
        return None
    rec = jsonable_row(rows[0])
    theme_rows = _q(
        """
SELECT t.theme_code
FROM trn_report_theme rt
JOIN mst_theme t ON t.theme_id = rt.theme_id
WHERE rt.report_id = CAST(:report_id AS integer)
ORDER BY t.group_order, t.theme_id
""",
        {"report_id": report_id},
    )
    theme_codes = [_blank(x.get("theme_code")) for x in theme_rows if _blank(x.get("theme_code"))]
    primary = _blank(rec.get("primary_theme_code"))
    if primary and primary not in theme_codes:
        theme_codes.insert(0, primary)
    return {
        "report_id": rec.get("report_id"),
        "report_code": _blank(rec.get("report_code")),
        "form_code": _blank(rec.get("form_code")),
        "fiscal_year_id": rec.get("fiscal_year_id"),
        "prefecture_code": _blank(rec.get("prefecture_code")),
        "shokokai_cd": _blank(rec.get("shokokai_cd")),
        "theme_id": rec.get("theme_id"),
        "industry": _blank(rec.get("industry")),
        "report_date": _fmt_date(rec.get("report_date")),
        "summary": _blank(rec.get("summary")),
        "content": _blank(rec.get("content")) or _blank(rec.get("summary")),
        "time_start": _blank(rec.get("time_start")),
        "time_end": _blank(rec.get("time_end")),
        "business_person": _blank(rec.get("business_person")),
        "business_name": _blank(rec.get("business_name")),
        "staff_main_name": _blank(rec.get("staff_main_name")),
        "staff_sub_name": _blank(rec.get("staff_sub_name")),
        "registered_at": _fmt_date(rec.get("registered_at")),
        "status": _blank(rec.get("status")),
        "form_full_label": _blank(rec.get("form_full_label")),
        "form_short_label": _blank(rec.get("form_short_label")),
        "primary_theme_code": primary,
        "theme_codes": theme_codes,
        "theme_label": _blank(rec.get("theme_label")),
    }


def set_list_result(jsonObj, rows):
    jsonObj.setHtml("dragB", json.dumps(rows, ensure_ascii=False, default=str))
    jsonObj.setValue("count", len(rows))
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)


def fail(jsonObj, message):
    jsonObj.setValue(utils.json_constant.JSONID_ERR, message)
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
    jsonObj.setHtml("dragB", "[]")