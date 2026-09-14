#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api177_vectorforminitMapper:
    def api177_vectorforminit(vector_collection_id):
        params = ["vector_collection_id"]
        values = [vector_collection_id]
        return utils.sql_utils.formatSQL("""SELECT :vectorcollectionid , name , vector_count , synced_date , status FROM trn_vector_collection WHERE vector_collection_id = %s;""",params,values)
