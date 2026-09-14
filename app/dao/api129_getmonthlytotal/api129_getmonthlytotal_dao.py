#Dao.vm common function
from app.mapper.api129_getmonthlytotal.api129_getmonthlytotal_mapper import api129_getmonthlytotalMapper
import utils.mysqldb_utils
import utils.date_util
 # api129_getmonthlytotal

class Api129GetmonthlytotalDao :

# 関数定義_SQL文_月次合計
     
    def api129_getmonthlytotal(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api129_getmonthlytotalMapper.api129_getmonthlytotal(dtoObj.prefecture_code,dtoObj.shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
