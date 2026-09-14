#Dao.vm common function
from app.mapper.api107_inserttrusteddevice.api107_inserttrusteddevice_mapper import api107_inserttrusteddeviceMapper
import utils.mysqldb_utils
import utils.date_util
 # api107_inserttrusteddevice

class Api107InserttrusteddeviceDao :

# 関数定義_SQL文_信頼端末発行
     
    def api107_inserttrusteddevice(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api107_inserttrusteddeviceMapper.api107_inserttrusteddevice(dtoObj.user_account_id,dtoObj.token_hash,dtoObj.expires_at),{'user_account_id':dtoObj.user_account_id,'token_hash':dtoObj.token_hash,'expires_at':dtoObj.expires_at})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
