from flask import session

import utils.config
import utils.json_constant
import utils.string_util
from app.service.loginapi.loginapi_service import apply_staff_login_session, _is_true

DEV_FIXED_OTP = "123456"


class Verify2faapiService:

    def verify2faapi(self, verify2faapi_dto, jsonObj):
        code = utils.string_util.changeNullToBlank(verify2faapi_dto.code).replace(" ", "")
        remember_device = verify2faapi_dto.rememberdevice
        pending = session.get("PENDING_LOGIN") or {}
        utils.config.global_log.debug("verify2faapi start")
        try:
            if not pending:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "⚠ 確認コードが正しくありません")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return
            if code != DEV_FIXED_OTP:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "⚠ 確認コードが正しくありません")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            remember = pending.get("remember")
            if _is_true(remember_device):
                remember = True
            apply_staff_login_session(pending, remember)
            jsonObj.setValue("username", pending.get("shokuin_kj") or pending.get("user_id") or "")
            jsonObj.setScript("OK", "./#home")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "認証に失敗しました。")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug("verify2faapi end")
