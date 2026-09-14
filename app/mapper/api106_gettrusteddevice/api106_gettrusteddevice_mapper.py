#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api106_gettrusteddeviceMapper:
    def api106_gettrusteddevice(user_account_id,token_hash):
        params = ["user_account_id","token_hash"]
        values = [user_account_id,token_hash]
        return utils.sql_utils.formatSQL("""SELECT trusted_device_id , :useraccountid , expires_at FROM trn_trusted_device td WHERE td.user_account_id = user_account_id AND td.:tokenhash = token_hash AND td.expires_at > CURRENT_TIMESTAMP;""",params,values)
