import hashlib
from datetime import datetime, timezone

from flask import request, session

import utils.config
import utils.json_constant
import utils.session_constant
import utils.string_util
from app.dao.api105_authenticateuser.api105_authenticateuser_dao import Api105AuthenticateuserDao
from app.dao.api106_gettrusteddevice.api106_gettrusteddevice_dao import Api106GettrusteddeviceDao
from app.dto.api105_authenticateuser.api105_authenticateuser_dto import Api105AuthenticateuserDto
from app.dto.api106_gettrusteddevice.api106_gettrusteddevice_dto import Api106GettrusteddeviceDto
from logger import currentLog
from utils.encrypt import verify_password


def _is_true(value):
    return str(value or "").strip().lower() in ("1", "true", "t", "yes", "on")


def _hash_device_token(token):
    token = str(token or "").strip()
    if not token:
        return ""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _parse_locked_until(value):
    if not value:
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        if not text:
            return None
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def apply_staff_login_session(account, remember=False):
    loginid = utils.string_util.changeNullToBlank(account.get("user_id"))
    name = utils.string_util.changeNullToBlank(account.get("shokuin_kj")) or loginid
    session[utils.session_constant.LANGUAGE_ID] = "JPN"
    session[utils.session_constant.USER_ID] = loginid
    session["LOGIN_USER_ID"] = loginid
    session[utils.session_constant.APP_USER_ID] = loginid
    session["USER_ACCOUNT_ID"] = utils.string_util.changeNullToBlank(account.get("user_account_id"))
    session["PREFECTURE_CODE"] = utils.string_util.changeNullToBlank(account.get("prefecture_code"))
    session["SHOKOKAI_CD"] = utils.string_util.changeNullToBlank(account.get("shokokai_cd"))
    session["ORGID"] = utils.string_util.changeNullToBlank(account.get("shokokai_cd"))
    session[utils.session_constant.USER_FLG] = "OK"
    session["USER_NAME1"] = name
    session["USER_NAME2"] = name
    session.pop("PENDING_LOGIN", None)
    session.permanent = _is_true(remember)
    # 顧客設計: 組織名・ユーザーを session に載せる
    try:
        from app.common.session import refresh_session_profile

        refresh_session_profile()
    except Exception as e:
        utils.config.global_log.error(e)
    utils.config.global_log = currentLog.getLog(loginid)


class LoginapiService:

    def loginapi(self, loginapi_dto, jsonObj):
        prefecture_code = utils.string_util.changeNullToBlank(loginapi_dto.prefecturecode)
        user_id = utils.string_util.changeNullToBlank(loginapi_dto.userid)
        input_password = loginapi_dto.password or ""
        remember = loginapi_dto.remember
        utils.config.global_log.debug("loginapi start")
        try:
            if utils.string_util.isNullOrBlank(prefecture_code) or utils.string_util.isNullOrBlank(user_id) or utils.string_util.isNullOrBlank(input_password):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "⚠ 入力内容をご確認ください")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            api105_authenticateuser = Api105AuthenticateuserDto.dict_to_json({})
            api105_authenticateuser.prefecturecode = prefecture_code
            api105_authenticateuser.userid = user_id
            rows = Api105AuthenticateuserDao().api105_authenticateuser(api105_authenticateuser) or []
            if not rows:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "会員Noかパスワードが間違っています。")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            rec = rows[0]
            locked_until = _parse_locked_until(utils.string_util.dict_get(rec, "locked_until"))
            if locked_until and locked_until > datetime.now(timezone.utc):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "ユーザーはロックされました。システム管理者に連絡してください。")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            stored_password = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "password"))
            if utils.string_util.isNullOrBlank(stored_password) or not verify_password(input_password, stored_password):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "会員Noかパスワードが間違っています。")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            account = {
                "user_account_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_account_id")),
                "prefecture_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) or prefecture_code,
                "shokokai_cd": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")),
                "user_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_id")) or user_id,
                "shokuin_kj": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokuin_kj")),
                "totp_secret": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "totp_secret")),
                "is_mfa_enabled": utils.string_util.dict_get(rec, "is_mfa_enabled"),
                "remember": remember,
            }

            trusted = False
            token_hash = _hash_device_token(request.cookies.get("trusted_device_token"))
            if token_hash and account["user_account_id"]:
                api106_gettrusteddevice = Api106GettrusteddeviceDto.dict_to_json({})
                api106_gettrusteddevice.useraccountid = account["user_account_id"]
                api106_gettrusteddevice.tokenhash = token_hash
                trusted_rows = Api106GettrusteddeviceDao().api106_gettrusteddevice(api106_gettrusteddevice) or []
                trusted = len(trusted_rows) > 0

            if _is_true(account["is_mfa_enabled"]) and not trusted:
                session["PENDING_LOGIN"] = account
                jsonObj.setValue("need_mfa", True)
                jsonObj.setValue("username", account["shokuin_kj"] or account["user_id"])
                jsonObj.setScript("OK", "./#verify-2fa")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
                return

            apply_staff_login_session(account, remember)
            jsonObj.setValue("need_mfa", False)
            jsonObj.setValue("username", session.get("USER_NAME1") or account["shokuin_kj"] or account["user_id"])
            jsonObj.setValue("userid", account["user_id"])
            jsonObj.setValue("orgname", session.get("ORG_NAME") or "")
            jsonObj.setValue("useraccountid", account["user_account_id"])
            jsonObj.setValue("user_account_id", account["user_account_id"])
            jsonObj.setValue("prefecturecode", account["prefecture_code"])
            jsonObj.setValue("shokokaicd", account["shokokai_cd"])
            jsonObj.setScript("OK", "./#home")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ログインに失敗しました。")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug("loginapi end")
