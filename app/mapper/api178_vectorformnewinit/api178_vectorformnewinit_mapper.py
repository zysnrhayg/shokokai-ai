#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api178_vectorformnewinitMapper:
    def api178_vectorformnewinit():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT 1 AS result;""",params,values)
