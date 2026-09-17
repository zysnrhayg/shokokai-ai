import utils.sql_utils

class accountdeleteapiMapper:
    def accountdeleteapi(user_account_id, deleted_by):
        params = ["user_account_id", "deleted_by"]
        values = [user_account_id, deleted_by]
        # 論理削除：status=0、user_id を解放（UNIQUE(prefecture_code,user_id) のため）、
        # deleted_at / deleted_by / updated_at / updated_by を更新
        return utils.sql_utils.formatSQL(
            """UPDATE mst_user_account SET
  status = 0,
  user_id = user_id || '__del__' || user_account_id::text,
  deleted_at = to_char(now(), 'YYYYMMDDHH24MISS'),
  deleted_by = CAST(NULLIF(:deleted_by, '') AS integer),
  updated_at = to_char(now(), 'YYYYMMDDHH24MISS'),
  updated_by = CAST(NULLIF(:deleted_by, '') AS integer)
WHERE user_account_id = CAST(:user_account_id AS integer)
  AND deleted_at IS NULL
RETURNING user_account_id""",
            params,
            values,
        )
