#Dao.vm common function
from app.mapper.api144_insertknowledgeentry.api144_insertknowledgeentry_mapper import api144_insertknowledgeentryMapper
import utils.mysqldb_utils
import utils.date_util
 # api144_insertknowledgeentry

class Api144InsertknowledgeentryDao :

# 関数定義_SQL文_知識データ登録
     
    def api144_insertknowledgeentry(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api144_insertknowledgeentryMapper.api144_insertknowledgeentry(dtoObj.knowledge_entry_id,dtoObj.knowledge_code,dtoObj.title,dtoObj.prefecture_code,dtoObj.theme,dtoObj.knowledge_document_id,dtoObj.status,dtoObj.body,dtoObj.created_by,dtoObj.updated_by),{'knowledge_entry_id':dtoObj.knowledge_entry_id,'knowledge_code':dtoObj.knowledge_code,'title':dtoObj.title,'prefecture_code':dtoObj.prefecture_code,'theme':dtoObj.theme,'knowledge_document_id':dtoObj.knowledge_document_id,'status':dtoObj.status,'body':dtoObj.body,'created_by':dtoObj.created_by,'updated_by':dtoObj.updated_by})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
