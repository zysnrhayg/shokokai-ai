#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api124_insertreportMapper:
    def api124_insertreport(report_code,form_code,fiscal_year_id,prefecture_code,shokokai_cd,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status):
        params = ["report_code","form_code","fiscal_year_id","prefecture_code","shokokai_cd","theme_id","industry","report_date","summary","content","time_start","time_end","business_person","business_name","staff_main_name","staff_sub_name","status"]
        values = [report_code,form_code,fiscal_year_id,prefecture_code,shokokai_cd,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_report ( :reportcode , :formcode , :fiscalyearid , :prefecturecode , :shokokaicd , :themeid , :industry , :reportdate , :summary , :content , :timestart , :timeend , :businessperson , :businessname , :staffmainname , :staffsubname , registered_at , :status ) VALUES ( report_code , form_code , fiscal_year_id , prefecture_code , shokokai_cd , theme_id , industry , report_date , summary , content , time_start , time_end , business_person , business_name , staff_main_name , staff_sub_name , CURRENT_DATE , status ) RETURNING report_id AS report_id""",params,values)
