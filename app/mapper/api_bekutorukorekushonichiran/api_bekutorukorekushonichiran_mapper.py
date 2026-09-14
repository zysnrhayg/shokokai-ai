#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_bekutorukorekushonichiranMapper:
    def api_bekutorukorekushonichiran():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT * FROM trn_vector_collection ORDER BY vector_collection_id;""",params,values)
