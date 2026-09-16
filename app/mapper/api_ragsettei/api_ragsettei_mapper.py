#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_ragsetteiMapper:
    def api_ragsettei():
        params = []
        values = []
        # RAG設定を取得する（cfg_rag_settingから最新1件、論理削除済みデータを除外）
        return utils.sql_utils.formatSQL("""SELECT rag_setting_id , embedding_model , vector_db , chunk_size , chunk_overlap , last_synced_at FROM cfg_rag_setting WHERE deleted_at IS NULL ORDER BY rag_setting_id DESC LIMIT 1 ;""",params,values)
