import utils.config
import threading
import utils.json_constant
from flask import session
from app.dao.accountdeleteapi.accountdeleteapi_dao import AccountdeleteapiDao
from app.dto.accountdeleteapi.accountdeleteapi_dto import AccountdeleteapiDto
import utils.string_util


class AccountdeleteapiService:

    def accountdeleteapi(self, accountdeleteapi_dto, jsonObj):
        USER_ACCOUNT_ID = accountdeleteapi_dto.useraccountid
        deleted_by = utils.string_util.changeNullToBlank(session.get("USER_ACCOUNT_ID", ""))
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows = AccountdeleteapiDao().accountdeleteapi(accountdeleteapi_dto, deleted_by)
            if rows is not None and len(rows) > 0:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "削除しました")
                jsonObj.setValue("useraccountid", utils.string_util.changeNullToBlank(utils.string_util.dict_get(rows[0], "user_account_id")))
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
            else:
                jsonObj.setValue(utils.json_constant.JSONID_ERR, "削除に失敗しました")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "削除に失敗しました")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
