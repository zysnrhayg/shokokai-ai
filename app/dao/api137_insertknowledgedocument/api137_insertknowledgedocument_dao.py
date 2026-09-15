#Dao.vm common function
from app.mapper.api137_insertknowledgedocument.api137_insertknowledgedocument_mapper import api137_insertknowledgedocumentMapper
import utils.mysqldb_utils
import utils.date_util
 # api137_insertknowledgedocument

class Api137InsertknowledgedocumentDao :

# 関数定義_SQL文_ナレッジ文書登録

    def api137_insertknowledgedocument(self,dtoObj) :
        # DTOのフィールドからSQLパラメータを取得する
        returnVal = utils.mysqldb_utils.querySQL(
            api137_insertknowledgedocumentMapper.api137_insertknowledgedocument(
                dtoObj.knowledgedocumentid,
                dtoObj.prefecturecode,
                dtoObj.documentcode,
                dtoObj.title,
                dtoObj.category,
                dtoObj.format
            ),
            {
                'knowledge_document_id': dtoObj.knowledgedocumentid,
                'prefecture_code': dtoObj.prefecturecode if dtoObj.prefecturecode else None,
                'document_code': dtoObj.documentcode,
                'title': dtoObj.title,
                'category': dtoObj.category,
                'format': dtoObj.format
            }
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
