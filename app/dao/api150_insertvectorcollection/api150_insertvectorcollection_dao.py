#Dao.vm common function
from app.mapper.api150_insertvectorcollection.api150_insertvectorcollection_mapper import api150_insertvectorcollectionMapper
import utils.mysqldb_utils
import utils.date_util
 # api150_insertvectorcollection

class Api150InsertvectorcollectionDao :

# 関数定義_SQL文_ベクトル登録

    def api150_insertvectorcollection(self,dtoObj) :
        # DTOのフィールド名（name, vectorcount, baselinevectorcount, status）を使用する
        # collection_codeはMapper側でCTE+UPDATEにより自動採番するためDTOから取得しない
        returnVal = utils.mysqldb_utils.querySQL(api150_insertvectorcollectionMapper.api150_insertvectorcollection(dtoObj.name,dtoObj.vectorcount,dtoObj.baselinevectorcount,dtoObj.status),{'name':dtoObj.name,'vector_count':dtoObj.vectorcount,'baseline_vector_count':dtoObj.baselinevectorcount,'status':dtoObj.status})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
