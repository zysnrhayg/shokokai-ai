#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api130_getexportformsMapper:
    def api130_getexportforms(fiscal_year_id):
        params = ["fiscal_year_id"]
        values = [fiscal_year_id]
        return utils.sql_utils.formatSQL("""SELECT form_code , short_label , full_label FROM mst_form f WHERE f.:fiscalyearid = fiscal_year_id AND f.badge_class IS NULL ORDER BY form_code""",params,values)
