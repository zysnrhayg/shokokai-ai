#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class getreportformsMapper:
    def getreportforms(fiscal_year_id):
        params = ["fiscal_year_id"]
        values = [fiscal_year_id]
        return utils.sql_utils.formatSQL("""SELECT t.form_code AS form_code , t.full_label AS full_label FROM ( SELECT '全様式G' AS form_code , '全様式G' AS full_label , 0 AS sort_no , '' AS form_code_order UNION ALL SELECT mst_form.form_code AS form_code , mst_form.full_label AS full_label , 1 AS sort_no , mst_form.form_code AS form_code_order FROM mst_form WHERE mst_form.:fiscalyearid = fiscal_year_id AND mst_form.badge_class IS NOT NULL AND mst_form.form_code != 'F' ) t ORDER BY t.sort_no , t.form_code_order;""",params,values)
