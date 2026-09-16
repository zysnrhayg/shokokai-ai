#Dao.vm common function
from app.mapper.api_knowledgedocumentversioninformation.api_knowledgedocumentversioninformation_mapper import api_knowledgedocumentversioninformationMapper
import utils.mysqldb_utils
import utils.date_util
 # api_knowledgedocumentversioninformation

class ApiKnowledgedocumentversioninformationDao :

# 関数定義_SQL文_ナレッジ文書バージョン情報更新
     
    def api_knowledgedocumentversioninformation(self,dtoObj) :
        # DTOのフィールド名（camelCase）を使用する
        returnVal = utils.mysqldb_utils.querySQL(api_knowledgedocumentversioninformationMapper.api_knowledgedocumentversioninformation(dtoObj.status,dtoObj.updatedby,dtoObj.knowledgedocumentid),{'status':dtoObj.status,'updated_by':dtoObj.updatedby,'knowledge_document_id':dtoObj.knowledgedocumentid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
