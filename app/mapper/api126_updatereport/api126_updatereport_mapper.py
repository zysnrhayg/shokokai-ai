#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api126_updatereportMapper:
    def api126_updatereport(form_code,fiscal_year_id,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status,report_id):
        params = ["form_code","fiscal_year_id","theme_id","industry","report_date","summary","content","time_start","time_end","business_person","business_name","staff_main_name","staff_sub_name","status","report_id"]
        values = [form_code,fiscal_year_id,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status,report_id]
        return utils.sql_utils.formatSQL("""UPDATE trn_report SET :formcode = form_code , :fiscalyearid = fiscal_year_id , :themeid = theme_id , :industry = industry , :reportdate = report_date , :summary = summary , :content = content , :timestart = time_start , :timeend = time_end , :businessperson = business_person , :businessname = business_name , :staffmainname = staff_main_name , :staffsubname = staff_sub_name , :status = status WHERE :reportid = report_id""",params,values)
