#Dao.vm common function
from app.mapper.api137_insertknowledgedocument.api137_insertknowledgedocument_mapper import api137_insertknowledgedocumentMapper
import utils.mysqldb_utils
import utils.date_util
 # api137_insertknowledgedocument

class Api137InsertknowledgedocumentDao :

# 関数定義_SQL文_ナレッジ文書登録
     
    def api137_insertknowledgedocument(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api137_insertknowledgedocumentMapper.api137_insertknowledgedocument(dtoObj.knowledge_document_id,dtoObj.uploaded_date,dtoObj.file_size_kb,dtoObj.status,dtoObj.file_path),{'knowledge_document_id':dtoObj.knowledge_document_id,'uploaded_date':dtoObj.uploaded_date,'file_size_kb':dtoObj.file_size_kb,'status':dtoObj.status,'file_path':dtoObj.file_path})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
