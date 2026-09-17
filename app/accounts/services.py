# Account list visibility (customer: get_visible_accounts)
# 全国 = 絞込なし / 県連 = 自県内かつ県連自身を除く / 商工会 = 自組織のみ
# UI の権限・ステータス・県・商工会・キーワード絞込は DB WHERE で実施する。

from flask import session

import utils.mysqldb_utils
import utils.string_util
from app.common.account_list_row import account_row_to_selmap

FEDERATION_DEFAULT = "0021"
NATIONAL_PREFECTURE_CODE = "00"

_VISIBLE_ACCOUNTS_SQL = """
SELECT mst_user_account.user_account_id
     , mst_user_account.prefecture_code
     , mst_user_account.shokokai_cd
     , mst_user_account.user_id
     , mst_user_account.shokuin_kj
     , mst_user_account.email
     , mst_user_account.status
     , mst_user_account.core_linked
     , mst_user_account.permission_level
     , mst_user_account.last_login_at
     , mst_prefecture.name AS prefecture_name
     , mst_shokokai.name AS shokokai_name
     , COALESCE(
         (
           SELECT array_agg(mst_qualification.qualification_code ORDER BY mst_qualification.qualification_code)
           FROM mst_user_account_qualification
           INNER JOIN mst_qualification
             ON mst_qualification.qualification_id = mst_user_account_qualification.qualification_id
           WHERE mst_user_account_qualification.user_account_id = mst_user_account.user_account_id
         ),
         ARRAY[]::text[]
       ) AS qualification_codes
FROM mst_user_account
INNER JOIN mst_prefecture
  ON mst_prefecture.prefecture_code = mst_user_account.prefecture_code
INNER JOIN mst_shokokai
  ON mst_shokokai.prefecture_code = mst_user_account.prefecture_code
 AND mst_shokokai.shokokai_cd = mst_user_account.shokokai_cd
WHERE mst_user_account.deleted_at IS NULL
{where_extra}
ORDER BY mst_prefecture.sort_order
       , mst_shokokai.sort_order NULLS FIRST
       , mst_user_account.user_id
{limit_offset}
"""


def _normalize_nonneg_int(value):
    """空なら None。それ以外は 0 以上の int。不正値は None。"""
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    try:
        n = int(s)
    except (TypeError, ValueError):
        return None
    if n < 0:
        return None
    return n


def get_federation_shokokai_cd():
    try:
        rows = utils.mysqldb_utils.result_to_list_of_dict(
            utils.mysqldb_utils.querySQL(
                """
SELECT setting_value
FROM cfg_system_setting
WHERE setting_code = :code
  AND deleted_at IS NULL
LIMIT 1
""",
                {"code": "federation_shokokai_cd"},
            )
        )
        if rows:
            value = utils.string_util.changeNullToBlank(rows[0].get("setting_value"))
            if value:
                return value
    except Exception:
        pass
    return FEDERATION_DEFAULT


def resolve_account_role(rolecode=""):
    """UI rolecode があれば優先。なければログイン組織から推定。"""
    role = utils.string_util.changeNullToBlank(rolecode)
    if role in ("national", "pref", "shokokai"):
        return role
    pref = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
    sho = utils.string_util.changeNullToBlank(session.get("SHOKOKAI_CD"))
    if pref == NATIONAL_PREFECTURE_CODE:
        return "national"
    if sho == get_federation_shokokai_cd():
        return "pref"
    return "shokokai"


def get_visible_accounts(
    rolecode="",
    limit=None,
    offset=None,
    permission_level="",
    status="",
    keyword="",
    filter_prefecture_code="",
    filter_shokokai_cd="",
    core_linked="",
):
    """
    ロール別可視範囲 + UI絞込条件でアカウント一覧を返す。
    Returns: (rows:list[dict], role:str, prefecture_code:str, shokokai_cd:str)
    """
    role = resolve_account_role(rolecode)
    pref = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
    sho = utils.string_util.changeNullToBlank(session.get("SHOKOKAI_CD"))
    federation_cd = get_federation_shokokai_cd()
    limit_n = _normalize_nonneg_int(limit)
    offset_n = _normalize_nonneg_int(offset)

    permission_level = utils.string_util.changeNullToBlank(permission_level)
    status = utils.string_util.changeNullToBlank(status)
    keyword = utils.string_util.changeNullToBlank(keyword)
    filter_prefecture_code = utils.string_util.changeNullToBlank(filter_prefecture_code)
    filter_shokokai_cd = utils.string_util.changeNullToBlank(filter_shokokai_cd)
    core_linked = utils.string_util.changeNullToBlank(core_linked)

    where_extra = ""
    params = {}
    if role == "national":
        # 全国連: ロール上の組織絞込なし（UIの県/商工会でさらに絞れる）
        pass
    elif role == "pref":
        # 県連: 自県内かつ県連自身を除く
        where_extra = """
 AND mst_user_account.prefecture_code = :scope_prefecture_code
 AND mst_user_account.shokokai_cd <> :federation_shokokai_cd
"""
        params = {
            "scope_prefecture_code": pref,
            "federation_shokokai_cd": federation_cd,
        }
    else:
        # 商工会: 自組織のみ
        where_extra = """
 AND mst_user_account.prefecture_code = :scope_prefecture_code
 AND mst_user_account.shokokai_cd = :scope_shokokai_cd
"""
        params = {
            "scope_prefecture_code": pref,
            "scope_shokokai_cd": sho,
        }

    # UI 絞込（ロール可視範囲の内側で DB 条件を追加）
    if role == "national" and filter_prefecture_code:
        where_extra += """
 AND mst_user_account.prefecture_code = :filter_prefecture_code
"""
        params["filter_prefecture_code"] = filter_prefecture_code
    if role in ("national", "pref") and filter_shokokai_cd:
        where_extra += """
 AND mst_user_account.shokokai_cd = :filter_shokokai_cd
"""
        params["filter_shokokai_cd"] = filter_shokokai_cd
    if permission_level:
        where_extra += """
 AND mst_user_account.permission_level = :filter_permission_level
"""
        params["filter_permission_level"] = permission_level
    if status != "":
        where_extra += """
 AND mst_user_account.status = CAST(:filter_status AS integer)
"""
        params["filter_status"] = status
    if core_linked != "":
        want = str(core_linked).lower() in ("1", "true", "t", "yes", "あり")
        where_extra += """
 AND mst_user_account.core_linked = CAST(:filter_core_linked AS boolean)
"""
        params["filter_core_linked"] = "true" if want else "false"
    if keyword:
        where_extra += """
 AND (
      mst_user_account.user_id ILIKE '%' || :filter_keyword || '%'
   OR mst_user_account.shokuin_kj ILIKE '%' || :filter_keyword || '%'
   OR mst_user_account.email ILIKE '%' || :filter_keyword || '%'
 )
"""
        params["filter_keyword"] = keyword

    # 顧客SQL: LIMIT %s OFFSET %s（未指定時は句ごと省略）
    limit_offset = ""
    if limit_n is not None:
        limit_offset += "\nLIMIT :limit"
        params["limit"] = limit_n
        if offset_n is not None:
            limit_offset += "\nOFFSET :offset"
            params["offset"] = offset_n

    sql = _VISIBLE_ACCOUNTS_SQL.format(where_extra=where_extra, limit_offset=limit_offset)
    raw_rows = utils.mysqldb_utils.result_to_list_of_dict(
        utils.mysqldb_utils.querySQL(sql, params)
    )
    rows = [account_row_to_selmap(entity) for entity in (raw_rows or [])]
    return rows, role, pref, sho
