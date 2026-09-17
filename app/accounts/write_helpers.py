# Helpers for account create / update / soft-delete.

import json

import utils.mysqldb_utils
import utils.string_util


def parse_qualification_codes(raw):
    if raw is None or raw == "":
        return []
    if isinstance(raw, (list, tuple)):
        return [str(x).strip() for x in raw if str(x).strip()]
    s = str(raw).strip()
    if not s:
        return []
    if s.startswith("["):
        try:
            arr = json.loads(s)
            if isinstance(arr, list):
                return [str(x).strip() for x in arr if str(x).strip()]
        except Exception:
            pass
    return [p.strip() for p in s.split(",") if p.strip()]


def find_live_account_id(prefecture_code, user_id, exclude_user_account_id=None):
    pref = utils.string_util.changeNullToBlank(prefecture_code)
    uid = utils.string_util.changeNullToBlank(user_id)
    if not pref or not uid:
        return None
    sql = """
SELECT user_account_id
FROM mst_user_account
WHERE prefecture_code = :prefecture_code
  AND user_id = :user_id
  AND deleted_at IS NULL
"""
    params = {"prefecture_code": pref, "user_id": uid}
    excl = utils.string_util.changeNullToBlank(exclude_user_account_id)
    if excl:
        sql += "\n  AND user_account_id <> CAST(:exclude_id AS integer)"
        params["exclude_id"] = excl
    sql += "\nLIMIT 1"
    rows = utils.mysqldb_utils.result_to_list_of_dict(
        utils.mysqldb_utils.querySQL(sql, params)
    )
    if not rows:
        return None
    return utils.string_util.changeNullToBlank(
        utils.string_util.dict_get(rows[0], "user_account_id")
    )


def replace_account_qualifications(user_account_id, codes):
    uid = utils.string_util.changeNullToBlank(user_account_id)
    if not uid:
        return
    code_list = parse_qualification_codes(codes)
    utils.mysqldb_utils.querySQL(
        """DELETE FROM mst_user_account_qualification
WHERE user_account_id = CAST(:user_account_id AS integer)""",
        {"user_account_id": uid},
    )
    for code in code_list:
        qrows = utils.mysqldb_utils.result_to_list_of_dict(
            utils.mysqldb_utils.querySQL(
                """SELECT qualification_id
FROM mst_qualification
WHERE deleted_at IS NULL
  AND qualification_code = :code
ORDER BY fiscal_year_id DESC
LIMIT 1""",
                {"code": code},
            )
        )
        if not qrows:
            continue
        qid = utils.string_util.changeNullToBlank(
            utils.string_util.dict_get(qrows[0], "qualification_id")
        )
        if not qid:
            continue
        utils.mysqldb_utils.querySQL(
            """INSERT INTO mst_user_account_qualification (user_account_id, qualification_id)
VALUES (CAST(:user_account_id AS integer), CAST(:qualification_id AS integer))
ON CONFLICT DO NOTHING""",
            {"user_account_id": uid, "qualification_id": qid},
        )
