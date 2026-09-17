import utils.config
import threading
import utils.json_constant
from flask import session
from app.accounts.services import resolve_account_role
from app.common.api_json import jsonable_rows
from app.knowledge.services import get_entries_with_themes
import utils.string_util


def _pref_filter_for_kenren(prefecture_code=""):
    """顧客設計：県連ロールのみ WHERE prefecture_code を付与する。"""
    if resolve_account_role() != "pref":
        return ""
    pref = utils.string_util.changeNullToBlank(prefecture_code)
    if pref:
        return pref
    return utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))


class KnowledgesearchapiService:

    def knowledgesearchapi(self, knowledgesearchapi_dto, jsonObj):
        keyword = utils.string_util.changeNullToBlank(
            getattr(knowledgesearchapi_dto, "keyword", "") or ""
        )
        prefecture_code = _pref_filter_for_kenren(
            getattr(knowledgesearchapi_dto, "prefecturecode", "") or ""
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows = get_entries_with_themes(
                keyword=keyword,
                prefecture_code=prefecture_code,
            )
            jsonObj.setValue("entries", jsonable_rows(rows))
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT,
                utils.json_constant.RUNRESULT_SUCCESS,
            )
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ナレッジ検索に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT,
                utils.json_constant.RUNRESULT_FAIL,
            )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
