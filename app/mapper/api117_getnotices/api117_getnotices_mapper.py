#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api117_getnoticesMapper:
    def api117_getnotices(role_code):
        params = ["role_code"]
        values = [role_code]
        return utils.sql_utils.formatSQL("""SELECT notice_id , title , content , :rolecode , end_at FROM trn_notice tn WHERE ( tn.role_code = role_code OR tn.role_code IS NULL OR tn.role_code = '' ) AND ( tn.start_at IS NULL OR tn.start_at <= CURRENT_TIMESTAMP ) AND ( tn.end_at IS NULL OR tn.end_at >= CURRENT_TIMESTAMP ) ORDER BY tn.start_at DESC NULLS LAST;""",params,values)
