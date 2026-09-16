#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api153_resyncvectorcollectionsMapper:
    def api153_resyncvectorcollections(vector_collection_id,vector_count):
        params = ["vector_collection_id","vector_count"]
        values = [vector_collection_id,vector_count]
        # 再同期：ベクトル数を更新し、ステータスを「同期済み」に設定する
        # 同時にcfg_rag_settingのlast_synced_atも更新する（最終同期日時として表示するため）
        # RETURNING句で更新件数を確認できるようにする
        return utils.sql_utils.formatSQL("""WITH v AS ( UPDATE trn_vector_collection SET vector_count = :vector_count , baseline_vector_count = :vector_count , status = '同期済み' , synced_date = CURRENT_DATE , updated_at = TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , updated_by = 1 WHERE vector_collection_id = :vector_collection_id RETURNING vector_collection_id ) , r AS ( UPDATE cfg_rag_setting SET last_synced_at = NOW ( ) WHERE rag_setting_id = ( SELECT rag_setting_id FROM trn_vector_collection WHERE vector_collection_id = :vector_collection_id ) RETURNING rag_setting_id ) SELECT v.vector_collection_id FROM v ;""",params,values)
