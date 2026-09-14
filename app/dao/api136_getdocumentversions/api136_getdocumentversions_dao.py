#Dao.vm common function
from app.mapper.api136_getdocumentversions.api136_getdocumentversions_mapper import api136_getdocumentversionsMapper
import utils.mysqldb_utils
import utils.date_util
 # api136_getdocumentversions

class Api136GetdocumentversionsDao :

# 関数定義_SQL文_ナレッジ文書版
     
    def api136_getdocumentversions(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api136_getdocumentversionsMapper.api136_getdocumentversions(dtoObj.knowledge_document_id),{'knowledge_document_id':dtoObj.knowledge_document_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
