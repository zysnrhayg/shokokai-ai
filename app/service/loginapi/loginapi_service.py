import hashlib
from datetime import datetime, timezone

from flask import request, session

import utils.config
import utils.json_constant
import utils.string_util
from app.common.session import apply_login_session, resolve_fe_role
from app.dao.api105_authenticateuser.api105_authenticateuser_dao import Api105AuthenticateuserDao
from app.dao.api106_gettrusteddevice.api106_gettrusteddevice_dao import Api106GettrusteddeviceDao
from app.dto.api105_authenticateuser.api105_authenticateuser_dto import Api105AuthenticateuserDto
from app.dto.api106_gettrusteddevice.api106_gettrusteddevice_dto import Api106GettrusteddeviceDto
from logger import currentLog
from utils.encrypt import verify_password

# 顧客設計：認証失敗は共通メッセージ（存在有無／パスワード不一致を区別しない）
LOGIN_AUTH_FAIL_MSG = "ユーザーIDまたはパスワードが正しくありません。"


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
    """互換ラッパ：顧客設計＋既存キーを session に載せる。"""
    profile = apply_login_session(account, remember)
    loginid = utils.string_util.changeNullToBlank(account.get("user_id"))
    utils.config.global_log = currentLog.getLog(loginid)
    return profile


def _set_login_success_payload(jsonObj, account, profile):
    role = (profile or {}).get("rolecode") or resolve_fe_role(
        account.get("prefecture_code"), account.get("shokokai_cd")
    )
    jsonObj.setValue("need_mfa", False)
    jsonObj.setValue("username", (profile or {}).get("username") or account.get("shokuin_kj") or account.get("user_id") or "")
    jsonObj.setValue("userid", account.get("user_id") or "")
    jsonObj.setValue("orgname", (profile or {}).get("orgname") or session.get("ORG_NAME") or "")
    jsonObj.setValue("useraccountid", account.get("user_account_id") or "")
    jsonObj.setValue("user_account_id", account.get("user_account_id") or "")
    jsonObj.setValue("prefecturecode", account.get("prefecture_code") or "")
    jsonObj.setValue("shokokaicd", account.get("shokokai_cd") or "")
    jsonObj.setValue("permissionlevel", (profile or {}).get("permissionlevel") or account.get("permission_level") or "")
    jsonObj.setValue("email", (profile or {}).get("email") or account.get("email") or "")
    jsonObj.setValue("rolecode", role)
    # 権限（組織）に応じた初期画面＝ホーム（ロール付き）
    jsonObj.setScript("OK", "./#home")
    jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)


class LoginapiService:

    def loginapi(self, loginapi_dto, jsonObj):
        prefecture_code = utils.string_util.changeNullToBlank(loginapi_dto.prefecturecode)
        user_id = utils.string_util.changeNullToBlank(loginapi_dto.userid)
        input_password = loginapi_dto.password or ""
        remember = loginapi_dto.remember
        utils.config.global_log.debug("loginapi start")
        try:
            # 入力チェック（必須）：県は既存維持、ユーザーID／パスワードは顧客設計どおり必須
            if utils.string_util.isNullOrBlank(prefecture_code):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "県を選択してください。")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return
            if utils.string_util.isNullOrBlank(user_id):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "ユーザーIDを入力してください。")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return
            if utils.string_util.isNullOrBlank(input_password):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "パスワードを入力してください。")
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            api105_authenticateuser = Api105AuthenticateuserDto.dict_to_json({})
            api105_authenticateuser.prefecturecode = prefecture_code
            api105_authenticateuser.userid = user_id
            rows = Api105AuthenticateuserDao().api105_authenticateuser(api105_authenticateuser) or []
            if not rows:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, LOGIN_AUTH_FAIL_MSG)
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            rec = rows[0]
            locked_until = _parse_locked_until(utils.string_util.dict_get(rec, "locked_until"))
            if locked_until and locked_until > datetime.now(timezone.utc):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, LOGIN_AUTH_FAIL_MSG)
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            stored_password = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "password"))
            if utils.string_util.isNullOrBlank(stored_password) or not verify_password(input_password, stored_password):
                jsonObj.setValue(utils.json_constant.JSONID_MSG, LOGIN_AUTH_FAIL_MSG)
                jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
                return

            account = {
                "user_account_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_account_id")),
                "prefecture_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) or prefecture_code,
                "shokokai_cd": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")),
                "user_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_id")) or user_id,
                "shokuin_kj": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokuin_kj")),
                "email": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "email")),
                "permission_level": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "permission_level")),
                "core_linked": utils.string_util.dict_get(rec, "core_linked"),
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

            profile = apply_staff_login_session(account, remember)
            _set_login_success_payload(jsonObj, account, profile)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ログインに失敗しました。")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug("loginapi end")
