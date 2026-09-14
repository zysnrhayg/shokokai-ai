#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api116_getrecentreportsMapper:
    def api116_getrecentreports(prefecture_code,shokokai_cd):
        params = ["prefecture_code","shokokai_cd"]
        values = [prefecture_code,shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT r.report_id , r.report_date , t.label AS theme_label , f.short_label AS form_label FROM trn_report r JOIN mst_theme t ON t.theme_id = r.theme_id JOIN mst_form f ON f.form_code = r.form_code AND f.fiscal_year_id = r.fiscal_year_id WHERE r.:prefecturecode = prefecture_code AND r.:shokokaicd = shokokai_cd ORDER BY r.report_date DESC LIMIT 10;""",params,values)
