#Dao.vm common function
from app.mapper.api149_getvectorcollectiondetail.api149_getvectorcollectiondetail_mapper import api149_getvectorcollectiondetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api149_getvectorcollectiondetail

class Api149GetvectorcollectiondetailDao :

# 関数定義_SQL文_ベクトル詳細
     
    def api149_getvectorcollectiondetail(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api149_getvectorcollectiondetailMapper.api149_getvectorcollectiondetail(dtoObj.vector_collection_id),{'vector_collection_id':dtoObj.vector_collection_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
