#Dao.vm common function
from app.mapper.api139_updateknowledgedocument.api139_updateknowledgedocument_mapper import api139_updateknowledgedocumentMapper
import utils.mysqldb_utils
import utils.date_util
 # api139_updateknowledgedocument

class Api139UpdateknowledgedocumentDao :

# 関数定義_SQL文_ナレッジ文書更新
     
    def api139_updateknowledgedocument(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api139_updateknowledgedocumentMapper.api139_updateknowledgedocument(dtoObj.title,dtoObj.prefecture_code,dtoObj.category,dtoObj.format,dtoObj.updated_by,dtoObj.knowledge_document_id),{'title':dtoObj.title,'prefecture_code':dtoObj.prefecture_code,'category':dtoObj.category,'format':dtoObj.format,'updated_by':dtoObj.updated_by,'knowledge_document_id':dtoObj.knowledge_document_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
