"""実績確認・帳票出力 (#monthly) サービス層（顧客設計: app/monthly/services.py）。

一覧: get_monthly_report_detail / get_themes_by_fiscal_year / get_monthly_report_total
Init/FiscalYear/CSV: build_* / set_*
帳票: routes.export_excel → app.common.excel_export.render_aggregate_excel
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
# 実施年月必須の月次集計様式（v_output_i2_excel 等）
MONTHLY_YEARMONTH_FORMS = frozenset(["I-2", "I-3", "I-4", "I-5"])
# 年次タブ（年度単位 VIEW・実施年月不要）
ANNUAL_AGGREGATE_FORMS = frozenset(["H", "I-1", "I-6", "I-7", "I-8"])


def is_report_form_code(form_code):
    code = _blank(form_code)
    return code == "F" or code.startswith("G-")


def _as_bool(v):
    if v is True:
        return True
    if v is False or v is None:
        return False
    s = str(v).strip().lower()
    return s in ("1", "t", "true", "yes")


def export_form_flags(form_code, is_day_batch=False):
    """cfg 定義に基づく帳票出力メタ（画面・API 共通）。"""
    code = _blank(form_code)
    annual = code in ANNUAL_AGGREGATE_FORMS
    requires_yearmonth = (code in MONTHLY_YEARMONTH_FORMS) or (
        is_report_form_code(code) and not annual
    )
    return {
        "period_group": "annual" if annual else "monthly",
        "requires_yearmonth": requires_yearmonth,
        "is_day_batch": _as_bool(is_day_batch),
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
    """年度別テーマ一覧（顧客設計: mst_theme）。全年度分を埋め込み用に返す。"""
    out = {}
    for fy in years or []:
        code = _blank(fy.get("fiscal_year_code"))
        fy_id = fy.get("fiscal_year_id")
        out[code] = []
        if fy_id in (None, "") or not code:
            continue
        rows = _q(
            """
SELECT fiscal_year_id, theme_id, theme_code, label
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
                    "theme_code": _blank(rec.get("theme_code")),
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
    """顧客設計どおり target_* IS NULL の組織合計行。"""
    if not prefecture_code or not shokokai_cd:
        return []
    rows = _q(
        """
SELECT year_month, support_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND target_prefecture_code IS NULL
  AND target_shokokai_cd IS NULL
  AND deleted_at IS NULL
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
SELECT d.form_code,
       COALESCE(f.short_label, d.form_code) AS short_label,
       COALESCE(f.full_label, d.form_code) AS full_label,
       d.is_day_batch
FROM cfg_excel_report_definition d
LEFT JOIN mst_form f
  ON f.form_code = d.form_code
 AND f.fiscal_year_id = d.fiscal_year_id
 AND f.deleted_at IS NULL
WHERE d.deleted_at IS NULL
"""
    if fiscal_year_id not in (None, ""):
        sql += "  AND d.fiscal_year_id = CAST(:fiscal_year_id AS integer)\n"
        params["fiscal_year_id"] = fiscal_year_id
    sql += "ORDER BY d.form_code, d.fiscal_year_id DESC"
    seen = set()
    out = []
    for rec in _q(sql, params):
        code = _blank(rec.get("form_code"))
        if not code or code in seen:
            continue
        seen.add(code)
        flags = export_form_flags(code, rec.get("is_day_batch"))
        out.append(
            {
                "form_code": code,
                "short_label": _blank(rec.get("short_label")),
                "full_label": _blank(rec.get("full_label")),
                **flags,
            }
        )
    return out


def export_forms_by_years(fy_list):
    """全年度分の帳票定義（クライアント側で年度切替するため埋め込み）。"""
    out = {}
    for fy in fy_list or []:
        code = _blank(fy.get("fiscal_year_code"))
        fy_id = fy.get("fiscal_year_id")
        if not code:
            continue
        out[code] = export_forms(fy_id) if fy_id not in (None, "") else []
    return out


def report_form_months(prefecture_code, shokokai_cd):
    """F/G 帳票ボタン判定用：登録済み報告書の form_code×年月。"""
    if not prefecture_code or not shokokai_cd:
        return []
    rows = _q(
        """
SELECT r.form_code,
       to_char(r.report_date, 'YYYY-MM') AS year_month
FROM trn_report r
WHERE r.prefecture_code = :prefecture_code
  AND r.shokokai_cd = :shokokai_cd
  AND r.status = '登録済み'
  AND r.form_code IS NOT NULL
  AND r.report_date IS NOT NULL
GROUP BY r.form_code, to_char(r.report_date, 'YYYY-MM')
ORDER BY r.form_code, year_month
""",
        {"prefecture_code": prefecture_code, "shokokai_cd": shokokai_cd},
    )
    out = []
    for rec in rows:
        code = _blank(rec.get("form_code"))
        ym = _ym(rec.get("year_month"))
        if not code or not ym:
            continue
        out.append({"form_code": code, "year_month": ym})
    return out


def _has_kpi_data(detail, year_month="", months=None):
    """一覧 KPI に件数>0 があるか（帳票ボタン表示用）。"""
    ym = _ym(year_month)
    if ym:
        for rec in detail or []:
            if _ym(rec.get("year_month")) == ym and _int(rec.get("support_count")) > 0:
                return True
        return False
    month_set = set(_ym(m) for m in (months or []) if _ym(m))
    for rec in detail or []:
        rec_ym = _ym(rec.get("year_month"))
        if month_set and rec_ym not in month_set:
            continue
        if _int(rec.get("support_count")) > 0:
            return True
    return False


def _has_report_data(prefecture_code, shokokai_cd, fiscal_year_id, form_code, year_month=""):
    """様式 F/G 用：登録済み報告書が存在するか。"""
    if not prefecture_code or not shokokai_cd or fiscal_year_id in (None, "") or not form_code:
        return False
    params = {
        "prefecture_code": prefecture_code,
        "shokokai_cd": shokokai_cd,
        "fiscal_year_id": fiscal_year_id,
        "form_code": form_code,
    }
    sql = """
SELECT 1 AS ok
FROM trn_report r
WHERE r.prefecture_code = :prefecture_code
  AND r.shokokai_cd = :shokokai_cd
  AND r.fiscal_year_id = CAST(:fiscal_year_id AS integer)
  AND r.form_code = :form_code
  AND r.status = '登録済み'
"""
    ym = _ym(year_month)
    if ym:
        sql += "  AND to_char(r.report_date, 'YYYY-MM') = :year_month\n"
        params["year_month"] = ym
    sql += "LIMIT 1"
    return bool(_q(sql, params))


def filter_export_forms_by_data(
    forms,
    prefecture_code,
    shokokai_cd,
    fiscal_year_id,
    detail,
    year_month="",
    fy_months=None,
    period_type="",
):
    """
    一覧にデータがある場合のみ帳票ボタンを返す。
    - 月次: 当該月（なければ年度内）の KPI>0 が前提。月次様式のみ。
    - 年次: 当該年度の KPI>0 が前提。年次様式のみ。
    - F/G: さらに当該様式の報告書が存在する場合のみ。
    """
    ym = _ym(year_month)
    period = _blank(period_type).lower()
    if period not in ("monthly", "annual"):
        period = "monthly" if ym else "annual"
    want_group = period

    if want_group == "monthly":
        if ym:
            if not _has_kpi_data(detail, year_month=ym):
                return []
        elif not _has_kpi_data(detail, months=fy_months):
            return []
    else:
        if not _has_kpi_data(detail, months=fy_months):
            return []

    out = []
    for form in forms or []:
        if (form.get("period_group") or "monthly") != want_group:
            continue
        code = _blank(form.get("form_code"))
        if not code:
            continue
        if is_report_form_code(code):
            # 月次タブは実施年月で報告書を絞る／年次タブに F/G は出さない
            if not _has_report_data(
                prefecture_code, shokokai_cd, fiscal_year_id, code, ym if want_group == "monthly" else ""
            ):
                continue
        out.append(form)
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
    """
    顧客設計: 全期間分を埋め込み、選択年度の切替はクライアント側 JS。
    filter_themes は互換のため残すが、一覧では常に全テーマを返す（0件除外しない）。
    """
    role, pref, sho = resolve_org(session, dto)
    fy_list = _fy_list()
    requested = (
        _blank(fiscal_year_code)
        or _g(dto, "fiscalyearcode", "fiscal_year_code")
    )
    current_fy = _find_fy(fy_list, code=requested) if requested else (fy_list[0] if fy_list else None)
    current_code = (current_fy or {}).get("fiscal_year_code") or ""
    fy_id = (current_fy or {}).get("fiscal_year_id") or ""
    detail = get_monthly_report_detail(pref, sho)
    themes = get_themes_by_fiscal_year(fy_list)
    ym = _ym(year_month) or _ym(_g(dto, "yearmonth", "year_month"))
    forms_by_year = export_forms_by_years(fy_list)
    return {
        "current_fiscal_year_code": current_code,
        "fiscal_years": fy_list,
        "themes_by_year": themes,
        "detail_rows": detail,
        "total_rows": get_monthly_report_total(pref, sho),
        "export_forms": forms_by_year.get(current_code) or export_forms(fy_id),
        "export_forms_by_year": forms_by_year,
        "report_form_months": report_form_months(pref, sho),
        "prefecturecode": pref,
        "shokokaicd": sho,
        "rolecode": role,
        "yearmonth": ym,
    }


def build_fiscal_year_payload(session, dto):
    """互換: 一覧はクライアント切替のため Init と同内容を返す。"""
    code = _g(dto, "fiscalyearcode", "fiscal_year_code")
    if not code:
        raise ValueError("fiscal_year_code is required")
    return build_init_payload(session, dto, fiscal_year_code=code)


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


def resolve_export_file(session, dto):
    """互換: app/monthly/routes.export_excel へ委譲。"""
    from app.monthly.routes import export_excel

    return export_excel(session, dto)


# --- 顧客設計書の関数名（④ 実績確認・帳票出力） ---


def get_monthly_report_detail(prefecture_code, shokokai_cd):
    """テーマ×年月の支援件数（trn_kpi_theme_breakdown）。"""
    return detail_rows(prefecture_code, shokokai_cd)


def get_themes_by_fiscal_year(years):
    """年度別テーマ一覧（mst_theme）。years は fiscal_year 辞書のリスト。"""
    return themes_for_years(years)


def get_monthly_report_total(prefecture_code, shokokai_cd):
    """合計行（trn_kpi_monthly_stat、target_* IS NULL）。"""
    return total_rows(prefecture_code, shokokai_cd)


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
    # 列はリクエストの対象年度（画面の current / selected 年度）
    fy_code_req = _g(dto, "fiscalyearcode", "fiscal_year_code")
    payload = build_init_payload(
        session, dto, fiscal_year_code=fy_code_req, filter_themes=False
    )
    fy_code = payload.get("current_fiscal_year_code") or fy_code_req or ""
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
