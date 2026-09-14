#Dao.vm common function
from app.mapper.api122_getreportdetail.api122_getreportdetail_mapper import api122_getreportdetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api122_getreportdetail

class Api122GetreportdetailDao :

# 関数定義_SQL文_報告書詳細
     
    def api122_getreportdetail(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api122_getreportdetailMapper.api122_getreportdetail(dtoObj.report_id),{'report_id':dtoObj.report_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
