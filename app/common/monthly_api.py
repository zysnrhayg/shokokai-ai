"""実績確認・帳票出力 (#monthly): Init / FiscalYear / Export helpers.

Init/FiscalYear: KPI tables (trn_kpi_theme_breakdown / trn_kpi_monthly_stat).
Export: download file from configured MONTHLY_REPORT_EXPORT_DIR
        (filename from cfg_excel_report_definition.template_filename).
CSV一覧: same shape as 一覧 (DB), 条件に関係なく（0件テーマ除外なし）。
"""
import json
import os
import zipfile

import utils.json_constant
import utils.mysqldb_utils as db
import utils.string_util
from app.common.dashboard_api import org_from_session
from app.common.reports_api import fiscal_years, iter_months
from config import settings as app_settings

# リポジトリ同梱の動作確認用 zip（中身は dummy/*.xlsx）
_DUMMY_TEMPLATES_ZIP = "dummy_templates.zip"
# DB 未登録時のフォールバック（ddl seed と同じ命名）
FALLBACK_TEMPLATE_BY_FORM = {
    "H": "report_h_template.xlsx",
    "I-1": "report_i1_template.xlsx",
    "I-2": "report_i2_template.xlsx",
    "I-3": "report_i3_template.xlsx",
    "I-4": "report_i4_template.xlsx",
    "I-5": "report_i5_template.xlsx",
    "I-6": "report_i6_template.xlsx",
    "I-7": "report_i7_template.xlsx",
    "I-8": "report_i8_template.xlsx",
}


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


def _ym(v):
    if v is None or v == "":
        return ""
    if hasattr(v, "strftime"):
        return v.strftime("%Y-%m")
    s = str(v).strip()
    if len(s) >= 7 and s[4] == "-":
        return s[:7]
    return s


def _int(v, default=0):
    try:
        if v is None or v == "":
            return default
        return int(v)
    except (TypeError, ValueError):
        return default


def resolve_org(session, dto):
    role = _g(dto, "rolecode", "role_code") or "shokokai"
    pref, sho = org_from_session(session, dto)
    if role == "national":
        pref = pref or "00"
        if pref != "00":
            pref = "00"
        sho = sho or "0021"
    elif role == "pref":
        if not sho:
            sho = "0021"
        if pref == "00":
            pref = ""
    return role, pref, sho


def _fy_list():
    years = fiscal_years()
    return [
        {
            "fiscal_year_id": y.get("fiscal_year_id"),
            "fiscal_year_code": _blank(y.get("fiscal_year_code")),
            "label": _blank(y.get("label")),
            "start_month": _blank(y.get("start_month")),
            "end_month": _blank(y.get("end_month")),
        }
        for y in years
    ]


def _find_fy(fy_list, code="", fy_id=""):
    code = _blank(code)
    fy_id = str(fy_id) if fy_id not in (None, "") else ""
    for y in fy_list:
        if code and y.get("fiscal_year_code") == code:
            return y
        if fy_id and str(y.get("fiscal_year_id") or "") == fy_id:
            return y
    return fy_list[0] if fy_list else None


def themes_for_years(years):
    out = {}
    for fy in years:
        code = _blank(fy.get("fiscal_year_code"))
        fy_id = fy.get("fiscal_year_id")
        out[code] = []
        if fy_id in (None, ""):
            continue
        rows = _q(
            """
SELECT theme_id, label
FROM mst_theme
WHERE deleted_at IS NULL
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
ORDER BY group_order, theme_id
""",
            {"fiscal_year_id": fy_id},
        )
        for rec in rows:
            out[code].append(
                {
                    "theme_id": rec.get("theme_id"),
                    "label": _blank(rec.get("label")),
                }
            )
    return out


def detail_rows(prefecture_code, shokokai_cd):
    if not prefecture_code or not shokokai_cd:
        return []
    rows = _q(
        """
SELECT theme_id, year_month, support_count
FROM trn_kpi_theme_breakdown
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND deleted_at IS NULL
ORDER BY year_month, theme_id
""",
        {"prefecture_code": prefecture_code, "shokokai_cd": shokokai_cd},
    )
    out = []
    for rec in rows:
        ym = _ym(rec.get("year_month"))
        if not ym:
            continue
        out.append(
            {
                "theme_id": rec.get("theme_id"),
                "year_month": ym,
                "support_count": _int(rec.get("support_count")),
            }
        )
    return out


def total_rows(prefecture_code, shokokai_cd):
    if not prefecture_code or not shokokai_cd:
        return []
    rows = _q(
        """
SELECT year_month, SUM(support_count) AS support_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_prefecture_code IS NULL
  AND target_shokokai_cd IS NULL
  AND deleted_at IS NULL
GROUP BY year_month
ORDER BY year_month
""",
        {"prefecture_code": prefecture_code, "shokokai_cd": shokokai_cd},
    )
    out = []
    for rec in rows:
        ym = _ym(rec.get("year_month"))
        if not ym:
            continue
        out.append(
            {
                "year_month": ym,
                "support_count": _int(rec.get("support_count")),
            }
        )
    return out


def export_forms(fiscal_year_id=""):
    params = {}
    sql = """
SELECT form_code, short_label, full_label
FROM mst_form
WHERE deleted_at IS NULL
  AND (badge_class IS NULL OR badge_class = '')
"""
    if fiscal_year_id not in (None, ""):
        sql += "  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)\n"
        params["fiscal_year_id"] = fiscal_year_id
    sql += "ORDER BY form_code, fiscal_year_id DESC"
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
            }
        )
    return out


def themes_nonzero_for_month(themes, detail, year_month):
    """Keep themes that have support_count > 0 in the given year_month (DB detail rows)."""
    ym = _ym(year_month)
    if not ym:
        return list(themes or [])
    nonzero = set()
    for rec in detail or []:
        if _ym(rec.get("year_month")) != ym:
            continue
        if _int(rec.get("support_count")) > 0:
            nonzero.add(rec.get("theme_id"))
            nonzero.add(str(rec.get("theme_id")))
    out = []
    for t in themes or []:
        tid = t.get("theme_id")
        if tid in nonzero or str(tid) in nonzero:
            out.append(t)
    return out


def themes_nonzero_for_year(themes, detail, months):
    """Keep themes that have any support_count > 0 within the fiscal-year months."""
    month_set = set(_ym(m) for m in (months or []) if _ym(m))
    if not month_set:
        return list(themes or [])
    totals = {}
    for rec in detail or []:
        ym = _ym(rec.get("year_month"))
        if ym not in month_set:
            continue
        tid = rec.get("theme_id")
        totals[tid] = totals.get(tid, 0) + _int(rec.get("support_count"))
    out = []
    for t in themes or []:
        tid = t.get("theme_id")
        if _int(totals.get(tid, 0)) > 0:
            out.append(t)
    return out


def build_init_payload(session, dto, fiscal_year_code="", year_month="", filter_themes=True):
    role, pref, sho = resolve_org(session, dto)
    fy_list = _fy_list()
    requested = (
        _blank(fiscal_year_code)
        or _g(dto, "fiscalyearcode", "fiscal_year_code")
    )
    current_fy = _find_fy(fy_list, code=requested) if requested else (fy_list[0] if fy_list else None)
    current_code = (current_fy or {}).get("fiscal_year_code") or ""
    fy_id = (current_fy or {}).get("fiscal_year_id") or ""
    detail = detail_rows(pref, sho)
    themes = themes_for_years(fy_list)
    ym = _ym(year_month) or _ym(_g(dto, "yearmonth", "year_month"))
    fy_months = []
    if current_fy:
        fy_months = list(
            iter_months(current_fy.get("start_month") or "", current_fy.get("end_month") or "")
        )
    if filter_themes and current_code:
        themes = dict(themes)
        if ym:
            # 月次：当該実施年月の支援件数が0のテーマは一覧から除外
            themes[current_code] = themes_nonzero_for_month(
                themes.get(current_code) or [], detail, ym
            )
        else:
            # 年次（対象年度）：当該年度合計が0のテーマは一覧から除外
            themes[current_code] = themes_nonzero_for_year(
                themes.get(current_code) or [], detail, fy_months
            )
    return {
        "current_fiscal_year_code": current_code,
        "fiscal_years": fy_list,
        "themes_by_year": themes,
        "detail_rows": detail,
        "total_rows": total_rows(pref, sho),
        "export_forms": export_forms(fy_id),
        "prefecturecode": pref,
        "shokokaicd": sho,
        "rolecode": role,
        "yearmonth": ym,
    }


def build_fiscal_year_payload(session, dto):
    code = _g(dto, "fiscalyearcode", "fiscal_year_code")
    if not code:
        raise ValueError("fiscal_year_code is required")
    # yearmonth あり→月次絞り込み / なし→対象年度の合計0テーマ除外
    payload = build_init_payload(
        session,
        dto,
        fiscal_year_code=code,
        year_month=_g(dto, "yearmonth", "year_month"),
    )
    if payload["current_fiscal_year_code"] != code:
        payload["current_fiscal_year_code"] = code
        payload["export_forms"] = []
    return payload


def export_dir():
    """Configured directory for monthly/annual report files (customer-uploaded later)."""
    configured = _blank(app_settings.get("MONTHLY_REPORT_EXPORT_DIR", "data/monthly_report_exports"))
    if not configured:
        configured = "data/monthly_report_exports"
    if os.path.isabs(configured):
        return os.path.normpath(configured)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.normpath(os.path.join(root, configured))


def _ensure_dummy_template(base_dir, template_name):
    """
    顧客ファイルが無いとき、同梱 dummy_templates.zip から該当 xlsx を展開する（テスト用）。
    zip 内パス: dummy/<template_name> または <template_name>
    """
    dest = os.path.join(base_dir, template_name)
    if os.path.isfile(dest):
        return dest
    zip_path = os.path.join(base_dir, _DUMMY_TEMPLATES_ZIP)
    if not os.path.isfile(zip_path):
        # 相対設定のフォールバック：プロジェクトルート直下も探す
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        alt = os.path.join(root, "data", "monthly_report_exports", _DUMMY_TEMPLATES_ZIP)
        if os.path.isfile(alt):
            zip_path = alt
        else:
            return ""
    member = "dummy/%s" % template_name
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            # Windows zip で区切りが \\ の場合にも対応
            norm = {n.replace("\\", "/"): n for n in names}
            if member not in norm:
                if template_name in norm:
                    member = template_name
                else:
                    return ""
                actual = norm[member]
            else:
                actual = norm[member]
            os.makedirs(base_dir, exist_ok=True)
            with zf.open(actual) as src, open(dest, "wb") as out:
                out.write(src.read())
    except Exception as e:
        try:
            import utils.config
            utils.config.global_log.error("dummy template extract failed: %s", e)
        except Exception:
            pass
        return ""
    return dest if os.path.isfile(dest) else ""


def _lookup_template_filename(form_code, fiscal_year_id):
    form_code = _blank(form_code)
    if not form_code:
        return ""
    if fiscal_year_id not in (None, ""):
        rows = _q(
            """
SELECT template_filename
FROM cfg_excel_report_definition
WHERE deleted_at IS NULL
  AND form_code = :form_code
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
LIMIT 1
""",
            {"form_code": form_code, "fiscal_year_id": fiscal_year_id},
        )
        if rows:
            name = _blank(rows[0].get("template_filename"))
            if name:
                return os.path.basename(name)
    return FALLBACK_TEMPLATE_BY_FORM.get(form_code, "")


def resolve_export_file(dto):
    """
    Resolve absolute path of the report file under MONTHLY_REPORT_EXPORT_DIR.
    Returns (abs_path, download_filename, form_code, fiscal_year_code).
    Raises FileNotFoundError / ValueError with user-facing Japanese message.
    """
    form_code = _g(dto, "formcode", "form_code")
    if form_code not in FALLBACK_TEMPLATE_BY_FORM:
        raise ValueError("未対応の帳票です")

    fy_list = _fy_list()
    fy_code = _g(dto, "fiscalyearcode", "fiscal_year_code")
    fy = _find_fy(fy_list, code=fy_code) if fy_code else (fy_list[0] if fy_list else None)
    fy_id = (fy or {}).get("fiscal_year_id") or ""
    fy_code_out = _blank((fy or {}).get("fiscal_year_code")) or fy_code

    template_name = _lookup_template_filename(form_code, fy_id)
    if not template_name:
        raise FileNotFoundError("帳票ファイルの定義がありません")

    # basename only — block path traversal
    template_name = os.path.basename(template_name.replace("\\", "/"))
    base = os.path.realpath(export_dir())
    abs_path = os.path.realpath(os.path.join(base, template_name))
    try:
        under_dir = os.path.commonpath([abs_path, base]) == base
    except ValueError:
        under_dir = False
    if not under_dir:
        raise ValueError("不正なファイルパスです")
    if not os.path.isfile(abs_path):
        # テスト用ダミー zip から展開を試みる
        extracted = _ensure_dummy_template(base, template_name)
        if extracted:
            abs_path = os.path.realpath(extracted)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(
            "帳票ファイルが見つかりません（%s）。アップロード後に再度お試しください。" % template_name
        )
    return abs_path, template_name, form_code, fy_code_out


def set_export_file_result(jsonObj, abs_path, filename, form_code, fiscal_year_code):
    # filepath is consumed by controller (send_file); stripped before JSON error responses
    jsonObj.setValue("filepath", abs_path)
    jsonObj.setValue("filename", filename)
    jsonObj.setValue("formcode", form_code)
    jsonObj.setValue("fiscalyearcode", fiscal_year_code)
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)


def _reiwa_label(year_month):
    parts = str(year_month or "").split("-")
    if len(parts) < 2:
        return str(year_month or "")
    try:
        y, m = int(parts[0]), int(parts[1])
    except (TypeError, ValueError):
        return str(year_month)
    return "令和%s年%s月" % (y - 2018, m)


def build_list_csv(session, dto):
    """
    Build CSV rows for 一覧（条件に関係なく）.
    Ignores 実施年月 / 0件テーマ除外; columns = full fiscal-year months.
    """
    # 画面の絞り込み条件は適用しない（文案: CSVは条件に関係なく一覧を出力）
    payload = build_init_payload(session, dto, filter_themes=False)
    fy_code = payload.get("current_fiscal_year_code") or ""
    fy = _find_fy(payload.get("fiscal_years") or [], code=fy_code)
    months = []
    if fy:
        months = list(iter_months(fy.get("start_month") or "", fy.get("end_month") or ""))
    themes = (payload.get("themes_by_year") or {}).get(fy_code) or []
    detail = payload.get("detail_rows") or []
    totals = payload.get("total_rows") or []

    detail_map = {}
    for rec in detail:
        key = "%s|%s" % (rec.get("theme_id"), rec.get("year_month"))
        detail_map[key] = _int(rec.get("support_count"))
    total_map = {rec.get("year_month"): _int(rec.get("support_count")) for rec in totals}

    header = ["支援テーマ"] + [_reiwa_label(ym) for ym in months] + ["累計"]
    rows = [header]
    for theme in themes:
        tid = theme.get("theme_id")
        line = [_blank(theme.get("label"))]
        row_sum = 0
        for ym in months:
            cnt = detail_map.get("%s|%s" % (tid, ym), 0)
            row_sum += cnt
            line.append(cnt)
        line.append(row_sum)
        rows.append(line)

    total_line = ["合計"]
    total_sum = 0
    for ym in months:
        cnt = total_map.get(ym, 0)
        total_sum += cnt
        total_line.append(cnt)
    total_line.append(total_sum)
    rows.append(total_line)

    filename = "報告実績の確認・月次／年次帳票を出力する.csv"
    return rows, filename


def set_csv_result(jsonObj, rows, filename):
    jsonObj.setHtml("dragB", json.dumps(rows, ensure_ascii=False, default=str))
    jsonObj.setValue("count", max(0, len(rows) - 1))
    jsonObj.setValue("filename", filename or "monthly.csv")
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)


def set_json_success(jsonObj, payload):
    for key, value in payload.items():
        jsonObj.setValue(key, value)
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)


def fail(jsonObj, message):
    jsonObj.setValue(utils.json_constant.JSONID_ERR, message)
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
