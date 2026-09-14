#Dao.vm common function
from app.mapper.api117_getnotices.api117_getnotices_mapper import api117_getnoticesMapper
import utils.mysqldb_utils
import utils.date_util
 # api117_getnotices

class Api117GetnoticesDao :

# 関数定義_SQL文_お知らせ
     
    def api117_getnotices(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api117_getnoticesMapper.api117_getnotices(dtoObj.role_code),{'role_code':dtoObj.role_code})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
