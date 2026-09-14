#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_knowledgedocumentversioninformationMapper:
    def api_knowledgedocumentversioninformation(status,updated_by,knowledge_document_id):
        params = ["status","updated_by","knowledge_document_id"]
        values = [status,updated_by,knowledge_document_id]
        return utils.sql_utils.formatSQL("""UPDATE trn_knowledge_document_version SET :status = %s , updated_at = TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , :updatedby = %s WHERE :knowledgedocumentid = %s AND version_number = ( SELECT active_version_number FROM trn_knowledge_document WHERE knowledge_document_id = %s ) ;""",params,values)
