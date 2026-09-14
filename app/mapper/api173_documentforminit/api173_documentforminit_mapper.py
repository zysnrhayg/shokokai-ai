#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api173_documentforminitMapper:
    def api173_documentforminit():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT vector_collection_id , collection_code , rag_setting_id , name , vector_count , baseline_vector_count , status , synced_date FROM public.trn_vector_collection;""",params,values)
