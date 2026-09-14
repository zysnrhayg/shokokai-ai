#Dao.vm common function
from app.mapper.api131_insertaccount.api131_insertaccount_mapper import api131_insertaccountMapper
import utils.mysqldb_utils
import utils.date_util
 # api131_insertaccount

class Api131InsertaccountDao :

# 関数定義_SQL文_アカウント登録
     
    def api131_insertaccount(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api131_insertaccountMapper.api131_insertaccount(dtoObj.prefecture_code,dtoObj.shokokai_cd,dtoObj.user_id,dtoObj.shokuin_kj,dtoObj.email,dtoObj.status,dtoObj.core_linked,dtoObj.permission_level,dtoObj.password),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd,'user_id':dtoObj.user_id,'shokuin_kj':dtoObj.shokuin_kj,'email':dtoObj.email,'status':dtoObj.status,'core_linked':dtoObj.core_linked,'permission_level':dtoObj.permission_level,'password':dtoObj.password})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
