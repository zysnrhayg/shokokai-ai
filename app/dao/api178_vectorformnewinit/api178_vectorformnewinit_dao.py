#Dao.vm common function
from app.mapper.api178_vectorformnewinit.api178_vectorformnewinit_mapper import api178_vectorformnewinitMapper
import utils.mysqldb_utils
import utils.date_util
 # api178_vectorformnewinit

class Api178VectorformnewinitDao :

# 関数定義_SQL文_ベクトル登録初期表示
     
    def api178_vectorformnewinit(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api178_vectorformnewinitMapper.api178_vectorformnewinit(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
