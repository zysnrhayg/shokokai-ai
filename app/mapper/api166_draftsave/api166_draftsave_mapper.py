#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api166_draftsaveMapper:
    def api166_draftsave(houkokushokoumokuisshiki):
        params = ["houkokushokoumokuisshiki"]
        values = [houkokushokoumokuisshiki]
        return utils.sql_utils.formatSQL("""SELECT 1 AS result""",params,values)
