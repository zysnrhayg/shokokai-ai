#Dao.vm common function
from app.mapper.api135_getknowledgedocumentdetail.api135_getknowledgedocumentdetail_mapper import api135_getknowledgedocumentdetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api135_getknowledgedocumentdetail

class Api135GetknowledgedocumentdetailDao :

# 関数定義_SQL文_ナレッジ文書詳細
     
    def api135_getknowledgedocumentdetail(self,dtoObj) :
        # DTOのknowledgedocumentidをSQLパラメータに渡す
        knowledge_document_id = dtoObj.knowledgedocumentid
        returnVal = utils.mysqldb_utils.querySQL(api135_getknowledgedocumentdetailMapper.api135_getknowledgedocumentdetail(knowledge_document_id),{'knowledge_document_id':knowledge_document_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
