import json
import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.api_json import jsonable_row
from app.dao.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_dao import (
    ApiJigyoshomeinokohokakonosodanrirekinamesDao,
)
from app.dto.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_dto import (
    ApiJigyoshomeinokohokakonosodanrirekinamesDto,
)
import utils.string_util


class JigyoshomeinokohokakonosodanrirekinamesapiService:

    def jigyoshomeinokohokakonosodanrirekinamesapi(self, jigyoshomeinokohokakonosodanrirekinamesapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            api_dto = ApiJigyoshomeinokohokakonosodanrirekinamesDto.dict_to_json({})
            # 組織情報（都道府県コード／商工会コード）を取得
            pref = utils.string_util.changeNullToBlank(
                getattr(jigyoshomeinokohokakonosodanrirekinamesapi_dto, "prefecturecode", "")
                or session.get("PREFECTURE_CODE")
                or ""
            )
            shokokai = utils.string_util.changeNullToBlank(
                getattr(jigyoshomeinokohokakonosodanrirekinamesapi_dto, "shokokaicd", "")
                or session.get("SHOKOKAI_CD")
                or ""
            )
            api_dto.prefecturecode = pref
            api_dto.shokokaicd = shokokai
            api_dto.limit = utils.string_util.changeNullToBlank(
                getattr(jigyoshomeinokohokakonosodanrirekinamesapi_dto, "limit", "")
            ) or "20"
            api_dto.keyword = utils.string_util.changeNullToBlank(
                getattr(jigyoshomeinokohokakonosodanrirekinamesapi_dto, "keyword", "")
            ) or "%"

            rows = ApiJigyoshomeinokohokakonosodanrirekinamesDao().api_jigyoshomeinokohokakonosodanrirekinames(api_dto) or []
            map_list = []
            for entity in rows:
                row = jsonable_row(entity if isinstance(entity, dict) else {})
                map_list.append(
                    {
                        "business_name": row.get("business_name") or "",
                        "last_report_date": row.get("last_report_date") or "",
                    }
                )
            jsonObj.setHtml("dragB", json.dumps(map_list, default=str, ensure_ascii=False))
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "事業所名候補の取得に失敗しました")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
