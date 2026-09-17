# 顧客設計: app/common/session.py
"""ログインセッションから組織・ユーザーを取得する。"""
from flask import session

import utils.mysqldb_utils as db
import utils.session_constant
import utils.string_util


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def _q(sql, params=None):
    return db.result_to_list_of_dict(db.querySQL(sql, params or {})) or []


def resolve_fe_role(prefecture_code="", shokokai_cd=""):
    """ログイン組織からフロントのロール（national／pref／shokokai）を決める。"""
    pref = _blank(prefecture_code)
    sho = _blank(shokokai_cd)
    if pref == "00":
        return "national"
    if sho == "0021":
        return "pref"
    return "shokokai"


def get_current_organization():
    """サイドバー用：現在ログイン組織（mst_shokokai）。"""
    pref = _blank(session.get("PREFECTURE_CODE") or session.get("prefecture_code"))
    sho = _blank(session.get("SHOKOKAI_CD") or session.get("shokokai_cd"))
    if not pref or not sho:
        return {}
    rows = _q(
        """
SELECT *
FROM mst_shokokai
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND deleted_at IS NULL
LIMIT 1
""",
        {"prefecture_code": pref, "shokokai_cd": sho},
    )
    return rows[0] if rows else {}


def get_current_user():
    """サイドバー用：現在ログインユーザー（mst_user_account）。"""
    account_id = _blank(session.get("USER_ACCOUNT_ID") or session.get("user_account_id"))
    if not account_id:
        return {}
    rows = _q(
        """
SELECT user_account_id
     , user_id
     , shokuin_kj
     , shokuin_kj AS name
     , email
     , permission_level
     , prefecture_code
     , shokokai_cd
     , core_linked
     , is_mfa_enabled
FROM mst_user_account
WHERE user_account_id = CAST(:user_account_id AS integer)
  AND deleted_at IS NULL
LIMIT 1
""",
        {"user_account_id": account_id},
    )
    return rows[0] if rows else {}


def apply_login_session(account, remember=False):
    """
    顧客設計の session 項目＋既存キーをまとめて設定する。
    account: mst_user_account 行相当の dict
    """
    loginid = _blank(account.get("user_id"))
    name = _blank(account.get("shokuin_kj")) or loginid
    pref = _blank(account.get("prefecture_code"))
    sho = _blank(account.get("shokokai_cd"))
    account_id = _blank(account.get("user_account_id"))
    permission = _blank(account.get("permission_level"))
    email = _blank(account.get("email"))
    core_linked = account.get("core_linked")
    is_mfa = account.get("is_mfa_enabled")

    # --- 既存（アプリ互換） ---
    session[utils.session_constant.LANGUAGE_ID] = "JPN"
    session[utils.session_constant.USER_ID] = loginid
    session["LOGIN_USER_ID"] = loginid
    session[utils.session_constant.APP_USER_ID] = loginid
    session["USER_ACCOUNT_ID"] = account_id
    session["PREFECTURE_CODE"] = pref
    session["SHOKOKAI_CD"] = sho
    session["ORGID"] = sho
    session[utils.session_constant.USER_FLG] = "OK"
    session["USER_NAME1"] = name
    session["USER_NAME2"] = name
    session["PERMISSION_LEVEL"] = permission
    session["EMAIL"] = email
    session["CORE_LINKED"] = bool(core_linked) if core_linked not in (None, "") else False
    session["IS_MFA_ENABLED"] = bool(is_mfa) if is_mfa not in (None, "") else False

    # --- 顧客設計キー（snake_case） ---
    session["user_account_id"] = account_id
    session["user_id"] = loginid
    session["shokuin_kj"] = name
    session["prefecture_code"] = pref
    session["shokokai_cd"] = sho
    session["permission_level"] = permission
    session["email"] = email
    session["core_linked"] = session["CORE_LINKED"]
    session["is_mfa_enabled"] = session["IS_MFA_ENABLED"]

    session.pop("PENDING_LOGIN", None)
    remember_on = str(remember or "").strip().lower() in ("1", "true", "t", "yes", "on")
    session.permanent = remember_on

    profile = refresh_session_profile()
    role = resolve_fe_role(pref, sho)
    session["ROLE_CODE"] = role
    session["role_code"] = role
    profile["rolecode"] = role
    return profile


def refresh_session_profile():
    """ログイン直後などに組織名・表示名を session へ書き込む。"""
    org = get_current_organization()
    user = get_current_user()
    org_name = _blank(org.get("name") or org.get("short_name"))
    user_id = _blank(user.get("user_id") or session.get("LOGIN_USER_ID") or session.get("USER_ID") or session.get("user_id"))
    user_name = _blank(user.get("name") or user.get("shokuin_kj") or session.get("USER_NAME1") or session.get("shokuin_kj"))
    permission = _blank(user.get("permission_level") or session.get("PERMISSION_LEVEL") or session.get("permission_level"))
    email = _blank(user.get("email") or session.get("EMAIL") or session.get("email"))
    if org_name:
        session["ORG_NAME"] = org_name
        session["org_name"] = org_name
    if user_id:
        session["LOGIN_USER_ID"] = user_id
        session["user_id"] = user_id
    if user_name:
        session["USER_NAME1"] = user_name
        session["USER_NAME2"] = user_name
        session["shokuin_kj"] = user_name
    if permission:
        session["PERMISSION_LEVEL"] = permission
        session["permission_level"] = permission
    if email:
        session["EMAIL"] = email
        session["email"] = email
    if user.get("core_linked") not in (None, ""):
        session["CORE_LINKED"] = bool(user.get("core_linked"))
        session["core_linked"] = session["CORE_LINKED"]
    if user.get("is_mfa_enabled") not in (None, ""):
        session["IS_MFA_ENABLED"] = bool(user.get("is_mfa_enabled"))
        session["is_mfa_enabled"] = session["IS_MFA_ENABLED"]
    return {
        "organization": org,
        "user": user,
        "orgname": org_name or _blank(session.get("ORG_NAME")),
        "userid": user_id,
        "username": user_name,
        "permissionlevel": permission or _blank(session.get("PERMISSION_LEVEL")),
        "email": email or _blank(session.get("EMAIL")),
        "rolecode": _blank(session.get("ROLE_CODE") or session.get("role_code"))
        or resolve_fe_role(
            session.get("PREFECTURE_CODE") or session.get("prefecture_code"),
            session.get("SHOKOKAI_CD") or session.get("shokokai_cd"),
        ),
    }
