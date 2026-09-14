#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api129_getmonthlytotalMapper:
    def api129_getmonthlytotal(prefecture_code,shokokai_cd):
        params = ["prefecture_code","shokokai_cd"]
        values = [prefecture_code,shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT year_month , support_count FROM trn_monthly_report_total mrt WHERE mrt.:prefecturecode = prefecture_code AND mrt.:shokokaicd = shokokai_cd ORDER BY year_month""",params,values)
