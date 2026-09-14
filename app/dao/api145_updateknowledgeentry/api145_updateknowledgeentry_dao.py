#Dao.vm common function
from app.mapper.api145_updateknowledgeentry.api145_updateknowledgeentry_mapper import api145_updateknowledgeentryMapper
import utils.mysqldb_utils
import utils.date_util
 # api145_updateknowledgeentry

class Api145UpdateknowledgeentryDao :

# 関数定義_SQL文_知識データ更新
     
    def api145_updateknowledgeentry(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api145_updateknowledgeentryMapper.api145_updateknowledgeentry(dtoObj.title,dtoObj.prefecture_code,dtoObj.theme,dtoObj.knowledge_document_id,dtoObj.status,dtoObj.body,dtoObj.updated_by,dtoObj.knowledge_entry_id),{'title':dtoObj.title,'prefecture_code':dtoObj.prefecture_code,'theme':dtoObj.theme,'knowledge_document_id':dtoObj.knowledge_document_id,'status':dtoObj.status,'body':dtoObj.body,'updated_by':dtoObj.updated_by,'knowledge_entry_id':dtoObj.knowledge_entry_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
