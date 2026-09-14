#Dao.vm common function
from app.mapper.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_mapper import api143_getknowledgeentrydetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api143_getknowledgeentrydetail

class Api143GetknowledgeentrydetailDao :

# 関数定義_SQL文_知識データ詳細
     
    def api143_getknowledgeentrydetail(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api143_getknowledgeentrydetailMapper.api143_getknowledgeentrydetail(dtoObj.knowledge_entry_id),{'knowledge_entry_id':dtoObj.knowledge_entry_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
