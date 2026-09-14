#Dao.vm common function
from app.mapper.api204_formexport.api204_formexport_mapper import api204_formexportMapper
import utils.mysqldb_utils
import utils.date_util
 # api204_formexport

class Api204FormexportDao :

# 関数定義_SQL文_FORMEXPORT204
     
    def api204_formexport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api204_formexportMapper.api204_formexport(dtoObj.report_id),{'report_id':dtoObj.report_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
