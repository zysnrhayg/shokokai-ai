# 顧客設計: app/manual_input/services.py
"""相談／報告書入力まわりの共通サービス。"""
import utils.mysqldb_utils as db
import utils.string_util


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def count_draft_reports(prefecture_code="", shokokai_cd="", fiscal_year_id=""):
    """下書き件数（0件のときは呼び出し側で非表示）。"""
    pref = _blank(prefecture_code)
    sho = _blank(shokokai_cd)
    fy = _blank(fiscal_year_id)
    if not pref or not sho:
        return 0
    params = {"prefecture_code": pref, "shokokai_cd": sho}
    sql = """
SELECT COUNT(*) AS c
FROM trn_report
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND status = '下書き'
  AND deleted_at IS NULL
"""
    if fy:
        sql += "  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)\n"
        params["fiscal_year_id"] = fy
    rows = db.result_to_list_of_dict(db.querySQL(sql, params)) or []
    if not rows:
        return 0
    try:
        return int(rows[0].get("c") or 0)
    except (TypeError, ValueError):
        return 0
