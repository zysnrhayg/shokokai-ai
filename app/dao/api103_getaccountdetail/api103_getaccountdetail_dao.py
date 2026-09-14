#Dao.vm common function
from app.mapper.api103_getaccountdetail.api103_getaccountdetail_mapper import api103_getaccountdetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api103_getaccountdetail

class Api103GetaccountdetailDao :

# 関数定義_SQL文_アカウント詳細
     
    def api103_getaccountdetail(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api103_getaccountdetailMapper.api103_getaccountdetail(dtoObj.user_account_id),{'user_account_id':dtoObj.user_account_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
