#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_ragsetteiMapper:
    def api_ragsettei():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT * FROM cfg_rag_setting ORDER BY rag_setting_id LIMIT 1;""",params,values)
