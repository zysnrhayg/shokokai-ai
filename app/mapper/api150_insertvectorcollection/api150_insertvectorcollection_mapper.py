#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api150_insertvectorcollectionMapper:
    def api150_insertvectorcollection(collection_code,name,vector_count,baseline_vector_count,status):
        params = ["collection_code","name","vector_count","baseline_vector_count","status"]
        values = [collection_code,name,vector_count,baseline_vector_count,status]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_vector_collection ( :collectioncode , rag_setting_id , :name , :vectorcount , :baselinevectorcount , :status , synced_date ) VALUES ( collection_code , ( SELECT rag_setting_id FROM mst_rag_setting ORDER BY rag_setting_id LIMIT 1 ) , name , vector_count , baseline_vector_count , status , CURRENT_DATE ) RETURNING vector_collection_id;""",params,values)
