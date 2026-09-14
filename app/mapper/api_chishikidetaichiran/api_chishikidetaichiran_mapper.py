#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_chishikidetaichiranMapper:
    def api_chishikidetaichiran():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT trn_knowledge_entry. * , trn_knowledge_document.title AS document_title , mst_prefecture.name AS prefecture_name FROM trn_knowledge_entry LEFT JOIN trn_knowledge_document ON trn_knowledge_document.knowledge_document_id = trn_knowledge_entry.knowledge_document_id LEFT JOIN mst_prefecture ON mst_prefecture.prefecture_code = trn_knowledge_entry.prefecture_code ORDER BY trn_knowledge_entry.knowledge_entry_id;""",params,values)
