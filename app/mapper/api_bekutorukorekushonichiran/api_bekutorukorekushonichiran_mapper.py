#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_bekutorukorekushonichiranMapper:
    def api_bekutorukorekushonichiran():
        params = []
        values = []
        # フロントエンド表示に必要なカラムを明示指定する（SELECT * を廃止）
        # 論理削除済みデータを除外する
        return utils.sql_utils.formatSQL("""SELECT vector_collection_id , rag_setting_id , collection_code , name , vector_count , baseline_vector_count , status , synced_date , updated_at FROM trn_vector_collection WHERE deleted_at IS NULL ORDER BY vector_collection_id ;""",params,values)
