# 顧客設計: app/common/session.py
"""ログインセッションから組織・ユーザーを取得する。"""
from flask import session

import utils.mysqldb_utils as db
import utils.string_util


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def _q(sql, params=None):
    return db.result_to_list_of_dict(db.querySQL(sql, params or {})) or []


def get_current_organization():
    """サイドバー用：現在ログイン組織（mst_shokokai）。"""
    pref = _blank(session.get("PREFECTURE_CODE"))
    sho = _blank(session.get("SHOKOKAI_CD"))
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
    account_id = _blank(session.get("USER_ACCOUNT_ID"))
    if not account_id:
        return {}
    rows = _q(
        """
SELECT user_account_id
     , user_id
     , shokuin_kj
     , shokuin_kj AS name
     , permission_level
     , prefecture_code
     , shokokai_cd
FROM mst_user_account
WHERE user_account_id = CAST(:user_account_id AS integer)
  AND deleted_at IS NULL
LIMIT 1
""",
        {"user_account_id": account_id},
    )
    return rows[0] if rows else {}


def refresh_session_profile():
    """ログイン直後などに組織名・表示名を session へ書き込む。"""
    org = get_current_organization()
    user = get_current_user()
    org_name = _blank(org.get("name") or org.get("short_name"))
    user_id = _blank(user.get("user_id") or session.get("LOGIN_USER_ID") or session.get("USER_ID"))
    user_name = _blank(user.get("name") or user.get("shokuin_kj") or session.get("USER_NAME1"))
    if org_name:
        session["ORG_NAME"] = org_name
    if user_id:
        session["LOGIN_USER_ID"] = user_id
    if user_name:
        session["USER_NAME1"] = user_name
        session["USER_NAME2"] = user_name
    if user.get("permission_level") not in (None, ""):
        session["PERMISSION_LEVEL"] = _blank(user.get("permission_level"))
    return {
        "organization": org,
        "user": user,
        "orgname": org_name or _blank(session.get("ORG_NAME")),
        "userid": user_id,
        "username": user_name,
        "permissionlevel": _blank(session.get("PERMISSION_LEVEL")),
    }
