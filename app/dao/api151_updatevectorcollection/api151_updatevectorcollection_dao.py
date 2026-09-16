#Dao.vm common function
from app.mapper.api151_updatevectorcollection.api151_updatevectorcollection_mapper import api151_updatevectorcollectionMapper
import utils.mysqldb_utils
import utils.date_util
 # api151_updatevectorcollection

class Api151UpdatevectorcollectionDao :

# 関数定義_SQL文_ベクトル更新

    def api151_updatevectorcollection(self,dtoObj) :
        # DTOのフィールド名（vectorcollectionid, vectorcount）を使用する
        returnVal = utils.mysqldb_utils.querySQL(api151_updatevectorcollectionMapper.api151_updatevectorcollection(dtoObj.name,dtoObj.vectorcount,dtoObj.status,dtoObj.vectorcollectionid),{'name':dtoObj.name,'vector_count':dtoObj.vectorcount,'status':dtoObj.status,'vector_collection_id':dtoObj.vectorcollectionid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
