#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api143_getknowledgeentrydetailMapper:
    def api143_getknowledgeentrydetail(knowledgeentryid):
        params = ["knowledgeentryid"]
        values = [knowledgeentryid]
        # 知識データ詳細を取得する（原本文書タイトル・県名を結合で取得する）
        return utils.sql_utils.formatSQL("""SELECT e.knowledge_entry_id , e.knowledge_code , e.title , e.prefecture_code , p.name AS prefecture_name , e.knowledge_document_id , d.title AS document_title , e.updated_date , e.status , e.content FROM trn_knowledge_entry e LEFT JOIN trn_knowledge_document d ON d.knowledge_document_id = e.knowledge_document_id LEFT JOIN mst_prefecture p ON p.prefecture_code = e.prefecture_code WHERE e.knowledge_entry_id = :knowledgeentryid;""",params,values)
