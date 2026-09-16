#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api151_updatevectorcollectionMapper:
    def api151_updatevectorcollection(name,vector_count,status,vector_collection_id):
        params = ["name","vector_count","status","vector_collection_id"]
        values = [name,vector_count,status,vector_collection_id]
        # UPDATE文：SET句は実際のカラム名を指定し、名前付きバインドを使用する
        # vector_countも更新対象に含める
        # RETURNING句で更新件数を確認できるようにする
        return utils.sql_utils.formatSQL("""UPDATE trn_vector_collection SET name = :name , vector_count = :vector_count , status = :status , updated_at = TO_CHAR( NOW( ) , 'YYYYMMDDHH24MISS' ) , updated_by = 1 WHERE vector_collection_id = :vector_collection_id RETURNING vector_collection_id ;""",params,values)
