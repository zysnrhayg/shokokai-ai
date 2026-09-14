#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api108_getfiscalyearsMapper:
    def api108_getfiscalyears():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT fiscal_year_id , fiscal_year_code , label , start_month , end_month FROM mst_fiscal_year ORDER BY fiscal_year_code DESC""",params,values)
