#Dao.vm common function
from app.mapper.api153_resyncvectorcollections.api153_resyncvectorcollections_mapper import api153_resyncvectorcollectionsMapper
import utils.mysqldb_utils
import utils.date_util
 # api153_resyncvectorcollections

class Api153ResyncvectorcollectionsDao :

# 関数定義_SQL文_ベクトル再同期
     
    def api153_resyncvectorcollections(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api153_resyncvectorcollectionsMapper.api153_resyncvectorcollections(dtoObj.vector_collection_id,dtoObj.vector_count),{'vector_collection_id':dtoObj.vector_collection_id,'vector_count':dtoObj.vector_count})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
