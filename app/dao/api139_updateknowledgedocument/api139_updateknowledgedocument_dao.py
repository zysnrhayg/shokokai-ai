#Dao.vm common function
from app.mapper.api139_updateknowledgedocument.api139_updateknowledgedocument_mapper import api139_updateknowledgedocumentMapper
import utils.mysqldb_utils
import utils.date_util
 # api139_updateknowledgedocument

class Api139UpdateknowledgedocumentDao :

# 関数定義_SQL文_ナレッジ文書更新
     
    def api139_updateknowledgedocument(self,dtoObj) :
        # DTOのフィールド名（camelCase）を使用する
        returnVal = utils.mysqldb_utils.querySQL(api139_updateknowledgedocumentMapper.api139_updateknowledgedocument(dtoObj.title,dtoObj.prefecturecode,dtoObj.category,dtoObj.format,dtoObj.updatedby,dtoObj.knowledgedocumentid),{'title':dtoObj.title,'prefecture_code':dtoObj.prefecturecode,'category':dtoObj.category,'format':dtoObj.format,'updated_by':dtoObj.updatedby,'knowledge_document_id':dtoObj.knowledgedocumentid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
