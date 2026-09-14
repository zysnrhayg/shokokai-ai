#Dao.vm common function
from app.mapper.api_ragsettei.api_ragsettei_mapper import api_ragsetteiMapper
import utils.mysqldb_utils
import utils.date_util
 # api_ragsettei

class ApiRagsetteiDao :

# 関数定義_SQL文_RAG設定
     
    def api_ragsettei(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api_ragsetteiMapper.api_ragsettei(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
