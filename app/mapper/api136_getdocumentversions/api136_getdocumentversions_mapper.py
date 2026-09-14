#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api136_getdocumentversionsMapper:
    def api136_getdocumentversions(knowledge_document_id):
        params = ["knowledge_document_id"]
        values = [knowledge_document_id]
        return utils.sql_utils.formatSQL("""SELECT knowledge_document_version_id , version_number , uploaded_date , uploaded_by , file_size_kb , status FROM mst_knowledge_document_version WHERE :knowledgedocumentid = knowledge_document_id ORDER BY version_number;""",params,values)
