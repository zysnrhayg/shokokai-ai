#Dao.vm common function
from app.mapper.api106_gettrusteddevice.api106_gettrusteddevice_mapper import api106_gettrusteddeviceMapper
import utils.mysqldb_utils
import utils.date_util
 # api106_gettrusteddevice

class Api106GettrusteddeviceDao :

# 関数定義_SQL文_信頼端末照合
     
    def api106_gettrusteddevice(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api106_gettrusteddeviceMapper.api106_gettrusteddevice(dtoObj.user_account_id,dtoObj.token_hash),{'user_account_id':dtoObj.user_account_id,'token_hash':dtoObj.token_hash})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
