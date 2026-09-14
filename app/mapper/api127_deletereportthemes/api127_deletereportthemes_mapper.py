#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api127_deletereportthemesMapper:
    def api127_deletereportthemes(report_id):
        params = ["report_id"]
        values = [report_id]
        return utils.sql_utils.formatSQL("""DELETE FROM trn_report_theme WHERE :reportid = report_id""",params,values)
