#Dao.vm common function
from app.mapper.api153_resyncvectorcollections.api153_resyncvectorcollections_mapper import api153_resyncvectorcollectionsMapper
import utils.mysqldb_utils
import utils.date_util
 # api153_resyncvectorcollections

class Api153ResyncvectorcollectionsDao :

# 関数定義_SQL文_ベクトル再同期

    def api153_resyncvectorcollections(self,dtoObj) :
        # DTOのフィールド名（vectorcollectionid, vectorcount）を使用する
        returnVal = utils.mysqldb_utils.querySQL(api153_resyncvectorcollectionsMapper.api153_resyncvectorcollections(dtoObj.vectorcollectionid,dtoObj.vectorcount),{'vector_collection_id':dtoObj.vectorcollectionid,'vector_count':dtoObj.vectorcount})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
