#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api125_insertreportthemeMapper:
    def api125_insertreporttheme(report_id,theme_id):
        params = ["report_id","theme_id"]
        values = [report_id,theme_id]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_report_theme ( :reportid , :themeid ) VALUES ( report_id , theme_id ) ON CONFLICT DO NOTHING""",params,values)
