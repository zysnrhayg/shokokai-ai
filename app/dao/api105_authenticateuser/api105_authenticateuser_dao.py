#Dao.vm common function
from app.mapper.api105_authenticateuser.api105_authenticateuser_mapper import api105_authenticateuserMapper
import utils.mysqldb_utils
import utils.date_util
 # api105_authenticateuser

class Api105AuthenticateuserDao :

# 関数定義_SQL文_職員アカウント認証
     
    def api105_authenticateuser(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api105_authenticateuserMapper.api105_authenticateuser(dtoObj.prefecture_code,dtoObj.user_id),{'prefecture_code':dtoObj.prefecture_code,'user_id':dtoObj.user_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
