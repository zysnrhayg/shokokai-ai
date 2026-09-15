#Mapper.vm common function mapper
import utils.sql_utils

class api131_insertaccountMapper:
    def api131_insertaccount(prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,core_linked,permission_level,password):
        params = ["prefecture_code","shokokai_cd","user_id","shokuin_kj","email","status","core_linked","permission_level","password"]
        values = [prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,core_linked,permission_level,password]
        return utils.sql_utils.formatSQL(
            """INSERT INTO mst_user_account (
  prefecture_code, shokokai_cd, user_id, shokuin_kj, email, status, core_linked, permission_level, password
) VALUES (
  :prefecture_code, :shokokai_cd, :user_id, :shokuin_kj, :email, CAST(:status AS integer), CAST(:core_linked AS boolean), :permission_level, :password
) RETURNING user_account_id""",
            params,
            values,
        )
