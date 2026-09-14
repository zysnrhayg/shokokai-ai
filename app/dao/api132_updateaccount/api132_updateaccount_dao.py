#Dao.vm common function
from app.mapper.api132_updateaccount.api132_updateaccount_mapper import api132_updateaccountMapper
import utils.mysqldb_utils
import utils.date_util
 # api132_updateaccount

class Api132UpdateaccountDao :

# 関数定義_SQL文_アカウント更新
     
    def api132_updateaccount(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api132_updateaccountMapper.api132_updateaccount(dtoObj.prefecture_code,dtoObj.shokokai_cd,dtoObj.user_id,dtoObj.shokuin_kj,dtoObj.email,dtoObj.status,dtoObj.permission_level,dtoObj.password,dtoObj.user_account_id),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd,'user_id':dtoObj.user_id,'shokuin_kj':dtoObj.shokuin_kj,'email':dtoObj.email,'status':dtoObj.status,'permission_level':dtoObj.permission_level,'password':dtoObj.password,'user_account_id':dtoObj.user_account_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
