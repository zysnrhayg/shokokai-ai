#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api120_getthemesMapper:
    def api120_getthemes(fiscal_year_id):
        params = ["fiscal_year_id"]
        values = [fiscal_year_id]
        return utils.sql_utils.formatSQL("""SELECT theme_id , theme_code , label , filter_group FROM mst_theme WHERE :fiscalyearid = fiscal_year_id ORDER BY group_order , theme_id""",params,values)
