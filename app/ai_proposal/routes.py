# 顧客設計: app/ai_proposal/routes.py show()
from flask import session

from app.accounts.services import resolve_account_role
from app.common.api_json import jsonable_rows
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.knowledge.services import get_entries_with_themes
import utils.mysqldb_utils
import utils.string_util


def _pref_filter_for_kenren(prefecture_code=""):
    """顧客設計：県連ロールのみ WHERE prefecture_code を付与する。"""
    if resolve_account_role() != "pref":
        return ""
    pref = utils.string_util.changeNullToBlank(prefecture_code)
    if pref:
        return pref
    return utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))


def _load_industries(fiscal_year_id=""):
    sql = """SELECT industry_code
     , label
     , sort_order
     , fiscal_year_id
FROM mst_industry
WHERE deleted_at IS NULL
ORDER BY sort_order , industry_code"""
    params = {}
    if fiscal_year_id not in (None, ""):
        sql = """SELECT industry_code
     , label
     , sort_order
     , fiscal_year_id
FROM mst_industry
WHERE deleted_at IS NULL
  AND fiscal_year_id = CAST(:fiscal_year_id AS integer)
ORDER BY sort_order , industry_code"""
        params = {"fiscal_year_id": str(fiscal_year_id)}
    rows = utils.mysqldb_utils.querySQL(sql, params)
    return utils.mysqldb_utils.result_to_list_of_dict(rows) or []


def show(mode="ai", prefecture_code="", fiscal_year_id=""):
    """AI相談 / ナレッジ検索の初期表示。mode=search と AI① は同一の get_entries_with_themes()。"""
    pref = _pref_filter_for_kenren(prefecture_code)
    entries = get_entries_with_themes(keyword="", prefecture_code=pref)
    result = {"entries": jsonable_rows(entries)}
    if str(mode).strip().lower() == "search":
        return result

    api120 = Api120GetthemesDto.dict_to_json({})
    api120.fiscalyearid = fiscal_year_id
    result["themes"] = jsonable_rows(Api120GetthemesDao().api120_getthemes(api120) or [])
    result["industries"] = jsonable_rows(_load_industries(fiscal_year_id))
    return result
