#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api128_getmonthlydetailMapper:
    def api128_getmonthlydetail(prefecture_code,shokokai_cd):
        params = ["prefecture_code","shokokai_cd"]
        values = [prefecture_code,shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT filter_group , year_month , support_count FROM trn_monthly_report_detail mrd WHERE mrd.:prefecturecode = prefecture_code AND mrd.:shokokaicd = shokokai_cd ORDER BY year_month , filter_group""",params,values)
