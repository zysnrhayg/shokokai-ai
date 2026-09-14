#Dao.vm common function
from app.mapper.api138_insertdocumentversion.api138_insertdocumentversion_mapper import api138_insertdocumentversionMapper
import utils.mysqldb_utils
import utils.date_util
 # api138_insertdocumentversion

class Api138InsertdocumentversionDao :

# 関数定義_SQL文_ナレッジ文書版登録
     
    def api138_insertdocumentversion(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api138_insertdocumentversionMapper.api138_insertdocumentversion(dtoObj.knowledge_document_id,dtoObj.prefecture_code,dtoObj.document_code,dtoObj.title,dtoObj.category,dtoObj.format,dtoObj.created_by,dtoObj.updated_by),{'knowledge_document_id':dtoObj.knowledge_document_id,'prefecture_code':dtoObj.prefecture_code,'document_code':dtoObj.document_code,'title':dtoObj.title,'category':dtoObj.category,'format':dtoObj.format,'created_by':dtoObj.created_by,'updated_by':dtoObj.updated_by})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
