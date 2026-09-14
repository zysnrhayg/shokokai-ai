#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api132_updateaccountMapper:
    def api132_updateaccount(prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,permission_level,password,user_account_id):
        params = ["prefecture_code","shokokai_cd","user_id","shokuin_kj","email","status","permission_level","password","user_account_id"]
        values = [prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,permission_level,password,user_account_id]
        return utils.sql_utils.formatSQL("""UPDATE mst_user_account SET :prefecturecode = %s , :shokokaicd = %s , :userid = %s , :shokuinkj = %s , :email = %s , :status = %s , :permissionlevel = %s , :password = CASE WHEN %s IS NULL OR %s = '' THEN password ELSE %s END WHERE :useraccountid = %s""",params,values)
