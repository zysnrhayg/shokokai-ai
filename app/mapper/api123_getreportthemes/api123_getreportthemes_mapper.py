#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api123_getreportthemesMapper:
    def api123_getreportthemes(report_id):
        params = ["report_id"]
        values = [report_id]
        return utils.sql_utils.formatSQL("""SELECT t.theme_id , t.theme_code , t.label FROM trn_report_theme rt JOIN mst_theme t ON t.theme_id = rt.theme_id WHERE rt.:reportid = report_id""",params,values)
