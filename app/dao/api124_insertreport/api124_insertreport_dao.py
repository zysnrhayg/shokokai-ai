#Dao.vm common function
from app.mapper.api124_insertreport.api124_insertreport_mapper import api124_insertreportMapper
import utils.mysqldb_utils
import utils.date_util
 # api124_insertreport

class Api124InsertreportDao :

# 関数定義_SQL文_報告書登録
     
    def api124_insertreport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api124_insertreportMapper.api124_insertreport(dtoObj.report_code,dtoObj.form_code,dtoObj.fiscal_year_id,dtoObj.prefecture_code,dtoObj.shokokai_cd,dtoObj.theme_id,dtoObj.industry,dtoObj.report_date,dtoObj.summary,dtoObj.content,dtoObj.time_start,dtoObj.time_end,dtoObj.business_person,dtoObj.business_name,dtoObj.staff_main_name,dtoObj.staff_sub_name,dtoObj.status),{'report_code':dtoObj.report_code,'form_code':dtoObj.form_code,'fiscal_year_id':dtoObj.fiscal_year_id,'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd,'theme_id':dtoObj.theme_id,'industry':dtoObj.industry,'report_date':dtoObj.report_date,'summary':dtoObj.summary,'content':dtoObj.content,'time_start':dtoObj.time_start,'time_end':dtoObj.time_end,'business_person':dtoObj.business_person,'business_name':dtoObj.business_name,'staff_main_name':dtoObj.staff_main_name,'staff_sub_name':dtoObj.staff_sub_name,'status':dtoObj.status})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
