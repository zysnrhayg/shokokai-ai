#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api122_getreportdetailMapper:
    def api122_getreportdetail(report_id):
        params = ["report_id"]
        values = [report_id]
        return utils.sql_utils.formatSQL("""SELECT trn_report.:reportid AS report_id , trn_report.report_code AS report_code , trn_report.form_code AS form_code , trn_report.fiscal_year_id AS fiscal_year_id , trn_report.prefecture_code AS prefecture_code , trn_report.shokokai_cd AS shokokai_cd , trn_report.theme_id AS theme_id , trn_report.industry AS industry , trn_report.report_date AS report_date , trn_report.summary AS summary , trn_report.content AS content , trn_report.time_start AS time_start , trn_report.time_end AS time_end , trn_report.business_person AS business_person , trn_report.business_name AS business_name , trn_report.staff_main_name AS staff_main_name , trn_report.staff_sub_name AS staff_sub_name , trn_report.registered_at AS registered_at , mst_form.full_label AS form_full_label , mst_theme.theme_code AS primary_theme_code FROM trn_report JOIN mst_form ON mst_form.form_code = trn_report.form_code AND mst_form.fiscal_year_id = trn_report.fiscal_year_id JOIN mst_theme ON mst_theme.theme_id = trn_report.theme_id WHERE trn_report.report_id = report_id""",params,values)
