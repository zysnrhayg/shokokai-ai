#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_genponbunshoichiranMapper:
    def api_genponbunshoichiran(prefecture_code):
        params = ["prefecture_code"]
        values = [prefecture_code]
        return utils.sql_utils.formatSQL("""SELECT trn_knowledge_document. * , trn_knowledge_document_version.uploaded_date , trn_knowledge_document_version.file_size_kb , trn_knowledge_document_version.status , trn_knowledge_document_version.file_path , mst_prefecture.name AS prefecture_name , (SELECT COUNT( * ) FROM trn_knowledge_entry WHERE trn_knowledge_entry.knowledge_document_id = trn_knowledge_document.knowledge_document_id ) AS linked_count FROM trn_knowledge_document JOIN trn_knowledge_document_version ON trn_knowledge_document_version.knowledge_document_id = trn_knowledge_document.knowledge_document_id AND trn_knowledge_document_version.version_number = trn_knowledge_document.active_version_number LEFT JOIN mst_prefecture ON mst_prefecture.prefecture_code = trn_knowledge_document.prefecture_code WHERE trn_knowledge_document.deleted_at IS NULL AND trn_knowledge_document_version.deleted_at IS NULL <ifprefecture_code> AND (trn_knowledge_document.prefecture_code IS NULL OR trn_knowledge_document.prefecture_code = :prefecture_code) </ifprefecture_code> ORDER BY trn_knowledge_document.knowledge_document_id;""",params,values)
