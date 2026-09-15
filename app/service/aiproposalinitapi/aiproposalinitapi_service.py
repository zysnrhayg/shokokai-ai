import utils.config
import threading
import utils.json_constant
import utils.mysqldb_utils
from app.common.api_json import jsonable_rows
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api154_getpublishedentries.api154_getpublishedentries_dao import Api154GetpublishedentriesDao
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api154_getpublishedentries.api154_getpublishedentries_dto import Api154GetpublishedentriesDto
import utils.string_util


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


class AiproposalinitapiService:

    def aiproposalinitapi(self, aiproposalinitapi_dto, jsonObj):
        FISCAL_YEAR_ID = aiproposalinitapi_dto.fiscalyearid
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            api154 = Api154GetpublishedentriesDto.dict_to_json({})
            api154.keyword = ""
            api154.prefecturecode = utils.string_util.changeNullToBlank(
                getattr(aiproposalinitapi_dto, "prefecturecode", "") or ""
            )
            entries = Api154GetpublishedentriesDao().api154_getpublishedentries(api154) or []

            api120 = Api120GetthemesDto.dict_to_json({})
            api120.fiscalyearid = FISCAL_YEAR_ID
            themes = Api120GetthemesDao().api120_getthemes(api120) or []

            industries = _load_industries(FISCAL_YEAR_ID)

            jsonObj.setValue("themes", jsonable_rows(themes))
            jsonObj.setValue("industries", jsonable_rows(industries))
            jsonObj.setValue("entries", jsonable_rows(entries))
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "初期表示に失敗しました")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
