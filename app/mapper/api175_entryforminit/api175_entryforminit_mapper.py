#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api175_entryforminitMapper:
    def api175_entryforminit():
        params = []
        values = []
        # 紐付ファイル選択用に原本文書一覧を取得する（実テーブルはtrn_knowledge_document）
        return utils.sql_utils.formatSQL("""SELECT knowledge_document_id , document_code , title , category , format , active_version_number , prefecture_code FROM trn_knowledge_document ORDER BY knowledge_document_id;""",params,values)
