#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_knowledgedocumentversioninformationMapper:
    def api_knowledgedocumentversioninformation(status,updated_by,knowledge_document_id):
        params = ["status","updated_by","knowledge_document_id"]
        values = [status,updated_by,knowledge_document_id]
        # 有効版のステータスを更新する（原本文書のactive_version_numberに該当する版）
        return utils.sql_utils.formatSQL("""UPDATE trn_knowledge_document_version SET status = :status , updated_at = TO_CHAR( NOW( ) , 'YYYYMMDDHH24MISS' ) , updated_by = :updated_by WHERE knowledge_document_id = :knowledge_document_id AND version_number = ( SELECT active_version_number FROM trn_knowledge_document WHERE knowledge_document_id = :knowledge_document_id ) ;""",params,values)
