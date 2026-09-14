#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api131_insertaccountMapper:
    def api131_insertaccount(prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,core_linked,permission_level,password):
        params = ["prefecture_code","shokokai_cd","user_id","shokuin_kj","email","status","core_linked","permission_level","password"]
        values = [prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,core_linked,permission_level,password]
        return utils.sql_utils.formatSQL("""INSERT INTO mst_user_account ( :prefecturecode , :shokokaicd , :userid , :shokuinkj , :email , :status , :corelinked , :permissionlevel , :password ) VALUES (prefecture_code , shokokai_cd , user_id , shokuin_kj , email , status , core_linked , permission_level , password ) RETURNING user_account_id""",params,values)
