#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api100_getprefecturenamesMapper:
    def api100_getprefecturenames():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT prefecture_code , name , short_name , region , sort_order , is_pseudo FROM mst_prefecture;""",params,values)
