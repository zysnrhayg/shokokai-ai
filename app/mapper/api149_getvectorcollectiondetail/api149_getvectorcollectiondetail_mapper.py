#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api149_getvectorcollectiondetailMapper:
    def api149_getvectorcollectiondetail(vector_collection_id):
        params = ["vector_collection_id"]
        values = [vector_collection_id]
        # SELECT句は実際のカラム名を指定し、WHERE句は名前付きバインド:vector_collection_idを使用する
        # 論理削除済みデータを除外する
        return utils.sql_utils.formatSQL("""SELECT vector_collection_id , rag_setting_id , collection_code , name , vector_count , baseline_vector_count , status , synced_date FROM trn_vector_collection WHERE vector_collection_id = :vector_collection_id AND deleted_at IS NULL ;""",params,values)
