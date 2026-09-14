#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api204_formexportMapper:
    def api204_formexport(report_id):
        params = ["report_id"]
        values = [report_id]
        return utils.sql_utils.formatSQL("""SELECT trn_report.:reportid , trn_report.report_code , trn_report.form_code , mst_form.full_label AS form_full_label , trn_report.report_date , trn_report.time_start , trn_report.time_end , trn_report.staff_main_name , trn_report.staff_sub_name , trn_report.industry , trn_report.business_name , trn_report.business_person , trn_report.content , trn_report.summary , trn_report.prefecture_code , trn_report.shokokai_cd FROM trn_report JOIN mst_form ON mst_form.form_code = trn_report.form_code AND mst_form.fiscal_year_id = trn_report.fiscal_year_id WHERE trn_report.report_id = report_id;""",params,values)
