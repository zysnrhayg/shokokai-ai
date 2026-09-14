#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api135_getknowledgedocumentdetailMapper:
    def api135_getknowledgedocumentdetail(knowledge_document_id):
        params = ["knowledge_document_id"]
        values = [knowledge_document_id]
        return utils.sql_utils.formatSQL("""SELECT d.title , d.prefecture_code , d.category , d.format , v.file_size_kb , v.uploaded_date , v.status , ( SELECT COUNT( * ) FROM trn_knowledge_entry e WHERE e.:knowledgedocumentid = d.knowledge_document_id ) AS linked_count FROM trn_knowledge_document d INNER JOIN trn_knowledge_document_version v ON v.knowledge_document_id = d.knowledge_document_id AND v.version_number = d.active_version_number WHERE d.knowledge_document_id = %s;""",params,values)
