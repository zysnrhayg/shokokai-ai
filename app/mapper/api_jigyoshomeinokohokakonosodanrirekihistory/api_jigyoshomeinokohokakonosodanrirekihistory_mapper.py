#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_jigyoshomeinokohokakonosodanrirekihistoryMapper:
    def api_jigyoshomeinokohokakonosodanrirekihistory(trn_report_prefecture_code,trn_report_shokokai_cd,trn_report_business_name,limit):
        params = ["trn_report_prefecture_code","trn_report_shokokai_cd","trn_report_business_name","limit"]
        values = [trn_report_prefecture_code,trn_report_shokokai_cd,trn_report_business_name,limit]
        return utils.sql_utils.formatSQL("""SELECT trn_report.report_id , trn_report.report_date , trn_report.summary , mst_form.short_label AS form_short_label , mst_form.badge_class AS form_badge_class , mst_theme.label AS theme_label FROM trn_report JOIN mst_form ON mst_form.form_code = trn_report.form_code AND mst_form.fiscal_year_id = trn_report.fiscal_year_id JOIN mst_theme ON mst_theme.theme_id = trn_report.theme_id WHERE :trnreportprefecturecode = %s AND :trnreportshokokaicd = %s AND :trnreportbusinessname = %s AND trn_report.status = '登録済み' ORDER BY trn_report.report_date DESC , trn_report.registered_at DESC :limit %s;""",params,values)
