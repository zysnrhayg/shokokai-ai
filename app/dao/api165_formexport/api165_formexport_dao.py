#Dao.vm common function
from app.mapper.api165_formexport.api165_formexport_mapper import api165_formexportMapper
import utils.mysqldb_utils
import utils.date_util
 # api165_formexport

class Api165FormexportDao :

# 関数定義_SQL文_FORMEXPORT
     
    def api165_formexport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api165_formexportMapper.api165_formexport(dtoObj.report_id),{'report_id':dtoObj.report_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
