#Mapper.vm common function mapper
import utils.sql_utils

class api132_updateaccountMapper:
    def api132_updateaccount(prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,permission_level,password,user_account_id):
        params = ["prefecture_code","shokokai_cd","user_id","shokuin_kj","email","status","permission_level","password","user_account_id"]
        values = [prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,permission_level,password,user_account_id]
        # password が空ならパスワード列を更新しない
        if password is None or str(password).strip() == "":
            sql = """UPDATE mst_user_account SET
  prefecture_code = :prefecture_code,
  shokokai_cd = :shokokai_cd,
  user_id = :user_id,
  shokuin_kj = :shokuin_kj,
  email = :email,
  status = CAST(:status AS integer),
  permission_level = :permission_level,
  updated_at = to_char(now(), 'YYYYMMDDHH24MISS')
WHERE user_account_id = CAST(:user_account_id AS integer)
  AND deleted_at IS NULL
RETURNING user_account_id"""
        else:
            sql = """UPDATE mst_user_account SET
  prefecture_code = :prefecture_code,
  shokokai_cd = :shokokai_cd,
  user_id = :user_id,
  shokuin_kj = :shokuin_kj,
  email = :email,
  status = CAST(:status AS integer),
  permission_level = :permission_level,
  password = :password,
  updated_at = to_char(now(), 'YYYYMMDDHH24MISS')
WHERE user_account_id = CAST(:user_account_id AS integer)
  AND deleted_at IS NULL
RETURNING user_account_id"""
        return utils.sql_utils.formatSQL(sql, params, values)
