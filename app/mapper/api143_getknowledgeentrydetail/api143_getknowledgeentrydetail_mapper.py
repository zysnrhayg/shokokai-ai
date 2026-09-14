#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api143_getknowledgeentrydetailMapper:
    def api143_getknowledgeentrydetail(knowledge_entry_id):
        params = ["knowledge_entry_id"]
        values = [knowledge_entry_id]
        return utils.sql_utils.formatSQL("""SELECT e.:knowledgeentryid , e.knowledge_code , e.title , e.prefecture_code , e.theme , e.knowledge_document_id , e.updated_at , e.status , e.body , d.title AS document_title , p.name AS prefecture_name FROM trn_knowledge_entry e LEFT JOIN trn_knowledge_document d ON d.knowledge_document_id = e.knowledge_document_id LEFT JOIN mst_prefecture p ON p.prefecture_code = e.prefecture_code WHERE e.knowledge_entry_id = %s;""",params,values)
