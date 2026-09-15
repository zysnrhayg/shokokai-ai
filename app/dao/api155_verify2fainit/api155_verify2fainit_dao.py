#Dao.vm common function
from app.mapper.api155_verify2fainit.api155_verify2fainit_mapper import api155_verify2fainitMapper
import utils.mysqldb_utils
import utils.date_util
 # api155_verify2fainit

class Api155Verify2fainitDao :

# 関数定義_SQL文_Verify2faInit
     
    def api155_verify2fainit(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api155_verify2fainitMapper.api155_verify2fainit(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
