#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api153_resyncvectorcollectionsMapper:
    def api153_resyncvectorcollections(vector_collection_id,vector_count):
        params = ["vector_collection_id","vector_count"]
        values = [vector_collection_id,vector_count]
        return utils.sql_utils.formatSQL("""UPDATE trn_vector_collection SET :vectorcount = vector_count , status = '同期済み' , synced_date = CURRENT_DATE WHERE :vectorcollectionid = vector_collection_id;""",params,values)
