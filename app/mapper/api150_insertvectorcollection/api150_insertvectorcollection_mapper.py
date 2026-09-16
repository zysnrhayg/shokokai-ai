#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api150_insertvectorcollectionMapper:
    def api150_insertvectorcollection(name,vector_count,baseline_vector_count,status):
        params = ["name","vector_count","baseline_vector_count","status"]
        values = [name,vector_count,baseline_vector_count,status]
        # collection_codeはCTE内でMAX(id)+1から「col-XXX」形式で生成する（固定値「col-000」による一意制約違反を回避）
        # rag_setting_idはcfg_rag_settingから最新1件を取得する（mst_rag_settingは存在しないため）
        # 論理削除項目（deleted_at, deleted_by）は初期値としてNULLを設定する
        return utils.sql_utils.formatSQL("""WITH next_id AS ( SELECT COALESCE ( MAX ( vector_collection_id ) , 0 ) + 1 AS next_id FROM trn_vector_collection ) , ins AS ( INSERT INTO trn_vector_collection ( rag_setting_id , collection_code , name , vector_count , baseline_vector_count , status , synced_date , created_at , created_by , updated_at , updated_by , deleted_at , deleted_by ) SELECT ( SELECT rag_setting_id FROM cfg_rag_setting WHERE deleted_at IS NULL ORDER BY rag_setting_id DESC LIMIT 1 ) , 'col-' || LPAD ( next_id :: text , 3 , '0' ) , :name , :vector_count , :baseline_vector_count , :status , CURRENT_DATE , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , 1 , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , 1 , NULL , NULL FROM next_id RETURNING vector_collection_id ) SELECT ins.vector_collection_id FROM ins ;""",params,values)
