#BasicService.vm
#make Service templete
import json
import utils.config
import threading
import utils.json_constant
from app.accounts.services import get_visible_accounts
import utils.string_util


class AccountsfilterapiService:

    # アカウント一覧絞込（ロール可視範囲 + UI条件を DB で適用）
    def accountsfilterapi(self, accountsfilterapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            map_list, role, pref, sho = get_visible_accounts(
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "rolecode", "")),
                getattr(accountsfilterapi_dto, "limit", ""),
                getattr(accountsfilterapi_dto, "offset", ""),
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "permissionlevel", "")),
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "status", "")),
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "keyword", "")),
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "prefecturecode", "")),
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "shokokaicd", "")),
                utils.string_util.changeNullToBlank(getattr(accountsfilterapi_dto, "corelinked", "")),
            )
            jsonObj.setHtml("dragB", json.dumps(map_list, ensure_ascii=False))
            jsonObj.setValue("rolecode", role)
            jsonObj.setValue("prefecturecode", pref)
            jsonObj.setValue("shokokaicd", sho)
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
