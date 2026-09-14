#Dao.vm common function
from app.mapper.api141_usedocumentversion.api141_usedocumentversion_mapper import api141_usedocumentversionMapper
import utils.mysqldb_utils
import utils.date_util
 # api141_usedocumentversion

class Api141UsedocumentversionDao :

# 関数定義_SQL文_ナレッジ文書版利用
     
    def api141_usedocumentversion(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api141_usedocumentversionMapper.api141_usedocumentversion(dtoObj.version_number,dtoObj.knowledge_document_id),{'version_number':dtoObj.version_number,'knowledge_document_id':dtoObj.knowledge_document_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
