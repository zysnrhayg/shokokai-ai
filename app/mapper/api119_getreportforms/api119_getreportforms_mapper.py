#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api119_getreportformsMapper:
    def api119_getreportforms(fiscal_year_id):
        params = ["fiscal_year_id"]
        values = [fiscal_year_id]
        return utils.sql_utils.formatSQL("""SELECT form_code , full_label , short_label FROM mst_form WHERE :fiscalyearid = fiscal_year_id AND badge_class IS NOT NULL ORDER BY form_code""",params,values)
