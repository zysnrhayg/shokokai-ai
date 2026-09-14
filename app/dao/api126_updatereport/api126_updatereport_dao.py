#Dao.vm common function
from app.mapper.api126_updatereport.api126_updatereport_mapper import api126_updatereportMapper
import utils.mysqldb_utils
import utils.date_util
 # api126_updatereport

class Api126UpdatereportDao :

# 関数定義_SQL文_報告書更新
     
    def api126_updatereport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api126_updatereportMapper.api126_updatereport(dtoObj.form_code,dtoObj.fiscal_year_id,dtoObj.theme_id,dtoObj.industry,dtoObj.report_date,dtoObj.summary,dtoObj.content,dtoObj.time_start,dtoObj.time_end,dtoObj.business_person,dtoObj.business_name,dtoObj.staff_main_name,dtoObj.staff_sub_name,dtoObj.status,dtoObj.report_id),{'form_code':dtoObj.form_code,'fiscal_year_id':dtoObj.fiscal_year_id,'theme_id':dtoObj.theme_id,'industry':dtoObj.industry,'report_date':dtoObj.report_date,'summary':dtoObj.summary,'content':dtoObj.content,'time_start':dtoObj.time_start,'time_end':dtoObj.time_end,'business_person':dtoObj.business_person,'business_name':dtoObj.business_name,'staff_main_name':dtoObj.staff_main_name,'staff_sub_name':dtoObj.staff_sub_name,'status':dtoObj.status,'report_id':dtoObj.report_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
