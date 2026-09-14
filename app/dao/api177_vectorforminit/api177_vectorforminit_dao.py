#Dao.vm common function
from app.mapper.api177_vectorforminit.api177_vectorforminit_mapper import api177_vectorforminitMapper
import utils.mysqldb_utils
import utils.date_util
 # api177_vectorforminit

class Api177VectorforminitDao :

# 関数定義_SQL文_ベクトル編集
     
    def api177_vectorforminit(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api177_vectorforminitMapper.api177_vectorforminit(dtoObj.vector_collection_id),{'vector_collection_id':dtoObj.vector_collection_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
