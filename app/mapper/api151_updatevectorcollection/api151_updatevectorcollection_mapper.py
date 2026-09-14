#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api151_updatevectorcollectionMapper:
    def api151_updatevectorcollection(name,status,vector_collection_id):
        params = ["name","status","vector_collection_id"]
        values = [name,status,vector_collection_id]
        return utils.sql_utils.formatSQL("""UPDATE trn_vector_collection SET :name = %s , vector_count = %s , synced_date = %s , :status = %s , updated_at = TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , updated_by = %s WHERE :vectorcollectionid = %s;""",params,values)
