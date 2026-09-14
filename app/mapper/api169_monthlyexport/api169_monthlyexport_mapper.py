#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api169_monthlyexportMapper:
    def api169_monthlyexport(form_code,fiscal_year_code):
        params = ["form_code","fiscal_year_code"]
        values = [form_code,fiscal_year_code]
        return utils.sql_utils.formatSQL("""SELECT 1 AS result""",params,values)
