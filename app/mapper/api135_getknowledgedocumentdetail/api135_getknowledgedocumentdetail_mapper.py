#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api135_getknowledgedocumentdetailMapper:
    def api135_getknowledgedocumentdetail(knowledge_document_id):
        params = ["knowledge_document_id"]
        values = [knowledge_document_id]
        # trn_knowledge_document と trn_knowledge_document_version を結合し、文書詳細情報を取得する
        # mst_prefecture から都道府県名を取得し、trn_knowledge_entry の件数は紐付け知識数として取得する
        return utils.sql_utils.formatSQL("""SELECT d.knowledge_document_id , d.document_code , d.title , d.category , d.format , d.active_version_number , d.prefecture_code , p.name AS prefecture_name , v.file_size_kb , v.uploaded_date , v.status , v.file_path , ( SELECT COUNT( * ) FROM trn_knowledge_entry e WHERE e.knowledge_document_id = d.knowledge_document_id ) AS linked_count FROM trn_knowledge_document d INNER JOIN trn_knowledge_document_version v ON v.knowledge_document_id = d.knowledge_document_id AND v.version_number = d.active_version_number LEFT JOIN mst_prefecture p ON p.prefecture_code = d.prefecture_code WHERE d.knowledge_document_id = :knowledge_document_id ;""",params,values)
