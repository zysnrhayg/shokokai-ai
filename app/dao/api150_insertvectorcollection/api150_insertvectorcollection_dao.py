#Dao.vm common function
from app.mapper.api150_insertvectorcollection.api150_insertvectorcollection_mapper import api150_insertvectorcollectionMapper
import utils.mysqldb_utils
import utils.date_util
 # api150_insertvectorcollection

class Api150InsertvectorcollectionDao :

# 関数定義_SQL文_ベクトル登録
     
    def api150_insertvectorcollection(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api150_insertvectorcollectionMapper.api150_insertvectorcollection(dtoObj.collection_code,dtoObj.name,dtoObj.vector_count,dtoObj.baseline_vector_count,dtoObj.status),{'collection_code':dtoObj.collection_code,'name':dtoObj.name,'vector_count':dtoObj.vector_count,'baseline_vector_count':dtoObj.baseline_vector_count,'status':dtoObj.status})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
