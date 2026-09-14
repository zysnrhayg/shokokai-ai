#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api105_authenticateuserMapper:
    def api105_authenticateuser(prefecture_code,user_id):
        params = ["prefecture_code","user_id"]
        values = [prefecture_code,user_id]
        return utils.sql_utils.formatSQL("""SELECT user_account_id , :prefecturecode , shokokai_cd , :userid , shokuin_kj , password , status , totp_secret , is_mfa_enabled , failed_login_count , locked_until FROM mst_user_account ua WHERE ua.prefecture_code = prefecture_code AND lower(ua.user_id ) = lower(user_id ) AND status = 1;""",params,values)
