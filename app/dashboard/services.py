# 顧客設計: app/dashboard/services.py
"""ホーム／ダッシュボード向けサービス関数。"""
from datetime import date

import utils.mysqldb_utils as db
import utils.string_util
from app.manual_input.services import count_draft_reports


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def _q(sql, params=None):
    return db.result_to_list_of_dict(db.querySQL(sql, params or {})) or []


def get_active_notices(role_code=""):
    """基本のお知らせ一覧（有効期間内のみ。権限 role_code で絞る）。"""
    rc = _blank(role_code)
    if not rc:
        return []
    # 顧客 mapper api_kihonnonshiraseichiran と同条件。日付未設定は ensure_notice_dates で補完後も NULL 可
    rows = _q(
        """
SELECT content
     , start_date
     , end_date
FROM trn_notice
WHERE deleted_at IS NULL
  AND role_code = :role_code
  AND (start_date IS NULL OR start_date <= CURRENT_DATE)
  AND (end_date IS NULL OR end_date >= CURRENT_DATE)
ORDER BY sort_order, notice_id
""",
        {"role_code": rc},
    )
    out = []
    for r in rows:
        content = _blank(r.get("content"))
        if not content:
            continue
        # 明示的に期限切れ（end_date < 今日）は出さない（上記 WHERE の二重防御）
        end_d = r.get("end_date")
        if end_d is not None and hasattr(end_d, "isoformat"):
            if end_d < date.today():
                continue
        out.append({"content": content})
    return out


def ensure_notice_dates():
    """日付未設定のお知らせに start/end を付与する（運用補完）。"""
    try:
        db.updateSQL(
            """
UPDATE trn_notice
SET start_date = COALESCE(start_date, CURRENT_DATE)
  , end_date = COALESCE(
        end_date,
        MAKE_DATE(
          EXTRACT(YEAR FROM CURRENT_DATE)::integer
            + CASE WHEN EXTRACT(MONTH FROM CURRENT_DATE) >= 4 THEN 1 ELSE 0 END,
          3,
          31
        )
      )
  , updated_at = TO_CHAR(NOW(), 'YYYYMMDDHH24MISS')
WHERE deleted_at IS NULL
  AND (start_date IS NULL OR end_date IS NULL)
""",
            {},
        )
    except Exception:
        # 起動時補完失敗は握りつぶし（表示側は NULL を有効扱い）
        pass


def get_current_month_support_count(prefecture_code="", shokokai_cd="", year_month=""):
    """今月の支援件数（trn_report をライブ集計）。"""
    pref = _blank(prefecture_code)
    sho = _blank(shokokai_cd)
    ym = _blank(year_month) or date.today().strftime("%Y-%m")
    if not pref or not sho:
        return 0
    rows = _q(
        """
SELECT COUNT(*) AS c
FROM trn_report
WHERE status = '登録済み'
  AND deleted_at IS NULL
  AND to_char(report_date, 'YYYY-MM') = :year_month
  AND prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
""",
        {"year_month": ym, "prefecture_code": pref, "shokokai_cd": sho},
    )
    if not rows:
        return 0
    try:
        return int(rows[0].get("c") or 0)
    except (TypeError, ValueError):
        return 0


def get_kpi_summaries_by_years(prefecture_code="", shokokai_cd="", fiscal_year_ids=None):
    """AI活用提案数（年度累計）。trn_kpi_monthly_stat.ai_activity_count を集計。"""
    pref = _blank(prefecture_code)
    sho = _blank(shokokai_cd)
    ids = [str(x).strip() for x in (fiscal_year_ids or []) if str(x).strip()]
    if not pref or not sho or not ids:
        return []
    # ANY 用に整数のみ許可
    safe_ids = []
    for i in ids:
        try:
            safe_ids.append(int(i))
        except (TypeError, ValueError):
            continue
    if not safe_ids:
        return []
    csv = ",".join(str(i) for i in safe_ids)
    rows = _q(
        f"""
SELECT fiscal_year_id
     , COALESCE(SUM(ai_activity_count), 0) AS ai_proposal_count
FROM trn_kpi_monthly_stat
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND fiscal_year_id = ANY(ARRAY[{csv}]::integer[])
  AND target_prefecture_code IS NULL
  AND target_shokokai_cd IS NULL
  AND deleted_at IS NULL
GROUP BY fiscal_year_id
""",
        {"prefecture_code": pref, "shokokai_cd": sho},
    )
    out = []
    for r in rows:
        out.append(
            {
                "fiscal_year_id": r.get("fiscal_year_id"),
                "ai_proposal_count": int(r.get("ai_proposal_count") or 0),
            }
        )
    return out


def get_recent_reports(prefecture_code="", shokokai_cd="", limit=4):
    """最近登録した報告（直近 N 件）。"""
    pref = _blank(prefecture_code)
    sho = _blank(shokokai_cd)
    lim = int(limit or 4)
    if not pref or not sho:
        return []
    rows = _q(
        """
SELECT trn_report.report_id
     , trn_report.report_code
     , trn_report.form_code
     , trn_report.report_date
     , trn_report.summary
     , trn_report.content
     , trn_report.support_content
     , trn_report.staff_main_name
     , trn_report.staff_sub_name
     , trn_report.business_name
     , trn_report.time_start
     , trn_report.time_end
     , trn_report.status
     , trn_report.registered_at
     , mst_theme.label AS theme_label
     , mst_theme.badge_class AS theme_badge_class
     , mst_form.short_label AS form_short_label
     , mst_form.badge_class AS form_badge_class
     , mst_industry.label AS industry
FROM trn_report
JOIN mst_theme ON mst_theme.theme_id = trn_report.theme_id
JOIN mst_form ON mst_form.form_code = trn_report.form_code
  AND mst_form.fiscal_year_id = trn_report.fiscal_year_id
LEFT JOIN mst_industry ON mst_industry.industry_code = trn_report.industry_code
  AND mst_industry.fiscal_year_id = trn_report.fiscal_year_id
WHERE trn_report.prefecture_code = :prefecture_code
  AND trn_report.shokokai_cd = :shokokai_cd
  AND trn_report.status = '登録済み'
  AND trn_report.deleted_at IS NULL
ORDER BY trn_report.registered_at DESC NULLS LAST
       , trn_report.report_date DESC NULLS LAST
LIMIT :lim
""",
        {"prefecture_code": pref, "shokokai_cd": sho, "lim": lim},
    )
    out = []
    for rec in rows:
        main = str(rec.get("staff_main_name") or "").strip()
        sub = str(rec.get("staff_sub_name") or "").strip()
        staff = main
        if sub:
            staff = (main + "／" + sub) if main else sub
        content = (
            str(rec.get("summary") or "").strip()
            or str(rec.get("content") or "").strip()[:80]
            or str(rec.get("support_content") or "").strip()[:80]
        )
        report_date = rec.get("report_date")
        if hasattr(report_date, "isoformat"):
            report_date = report_date.isoformat()
        out.append(
            {
                "report_id": rec.get("report_id"),
                "report_date": report_date or "",
                "form_code": str(rec.get("form_code") or ""),
                "form_label": str(rec.get("form_short_label") or rec.get("form_code") or ""),
                "badge_class": str(rec.get("form_badge_class") or "#1a6fa8"),
                "theme_label": str(rec.get("theme_label") or ""),
                "content": content,
                "staff": staff,
                "business_name": str(rec.get("business_name") or ""),
                "time_start": str(rec.get("time_start") or ""),
                "time_end": str(rec.get("time_end") or ""),
                "status": str(rec.get("status") or ""),
                "industry": str(rec.get("industry") or ""),
            }
        )
    return out


# re-export for callers that import draft helper via dashboard package
__all__ = [
    "get_active_notices",
    "ensure_notice_dates",
    "get_current_month_support_count",
    "get_kpi_summaries_by_years",
    "get_recent_reports",
    "count_draft_reports",
]
