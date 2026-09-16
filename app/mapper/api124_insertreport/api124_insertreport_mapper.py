#Mapper.vm common function mapper
# 報告書登録用マッパー：trn_reportへINSERTする
# 備考：DDL定義のカラム名は industry_code（industryではない）
import utils.sql_utils

class api124_insertreportMapper:
    def api124_insertreport(report_code,form_code,fiscal_year_id,prefecture_code,shokokai_cd,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status):
        params = ["report_code","form_code","fiscal_year_id","prefecture_code","shokokai_cd","theme_id","industry","report_date","summary","content","time_start","time_end","business_person","business_name","staff_main_name","staff_sub_name","status"]
        values = [report_code,form_code,fiscal_year_id,prefecture_code,shokokai_cd,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_report (
    report_code, form_code, fiscal_year_id, prefecture_code, shokokai_cd, theme_id, industry_code, report_date, summary, content, time_start, time_end, business_person, business_name, staff_main_name, staff_sub_name, registered_at, status, created_at, updated_at
) VALUES (
    :report_code, :form_code, CAST(:fiscal_year_id AS integer), :prefecture_code, :shokokai_cd, CAST(:theme_id AS integer), :industry, CAST(:report_date AS date), :summary, :content, :time_start, :time_end, :business_person, :business_name, :staff_main_name, :staff_sub_name, CURRENT_DATE, :status, to_char(now(), 'YYYYMMDDHH24MISS'), to_char(now(), 'YYYYMMDDHH24MISS')
) RETURNING report_id""",params,values)
