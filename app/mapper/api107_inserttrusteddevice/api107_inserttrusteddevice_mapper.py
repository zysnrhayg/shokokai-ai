#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api107_inserttrusteddeviceMapper:
    def api107_inserttrusteddevice(user_account_id,token_hash,expires_at):
        params = ["user_account_id","token_hash","expires_at"]
        values = [user_account_id,token_hash,expires_at]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_trusted_device ( :useraccountid , :tokenhash , created_at , :expiresat ) VALUES (user_account_id , token_hash , CURRENT_TIMESTAMP , expires_at ) ;""",params,values)
