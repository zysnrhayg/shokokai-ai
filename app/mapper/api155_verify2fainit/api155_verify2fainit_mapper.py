#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api155_verify2fainitMapper:
    def api155_verify2fainit():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT 1 AS result""",params,values)
