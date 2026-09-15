#Dao.vm common function
from app.mapper.api138_insertdocumentversion.api138_insertdocumentversion_mapper import api138_insertdocumentversionMapper
import utils.mysqldb_utils
import utils.date_util
 # api138_insertdocumentversion

class Api138InsertdocumentversionDao :

# 関数定義_SQL文_ナレッジ文書版登録

    def api138_insertdocumentversion(self,dtoObj) :
        # DTOのフィールドからSQLパラメータを取得する
        returnVal = utils.mysqldb_utils.querySQL(
            api138_insertdocumentversionMapper.api138_insertdocumentversion(
                dtoObj.knowledgedocumentid,
                dtoObj.versionnumber,
                dtoObj.uploadedby,
                dtoObj.filesizekb,
                dtoObj.status,
                dtoObj.filepath
            ),
            {
                'knowledge_document_id': dtoObj.knowledgedocumentid,
                'version_number': dtoObj.versionnumber,
                'uploaded_by': dtoObj.uploadedby,
                'file_size_kb': dtoObj.filesizekb if dtoObj.filesizekb else 0,
                'status': dtoObj.status,
                'file_path': dtoObj.filepath
            }
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
