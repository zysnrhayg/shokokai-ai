#Dao.vm common function
from app.mapper.api_chishikidetaichiran.api_chishikidetaichiran_mapper import api_chishikidetaichiranMapper
import utils.mysqldb_utils
import utils.date_util
 # api_chishikidetaichiran

class ApiChishikidetaichiranDao :

# 関数定義_SQL文_知識データ一覧
     
    def api_chishikidetaichiran(self,dtoObj) :
        prefecture_code = (
            getattr(dtoObj, "prefecturecode", None)
            or getattr(dtoObj, "prefecture_code", None)
            or ""
        )
        returnVal = utils.mysqldb_utils.querySQL(api_chishikidetaichiranMapper.api_chishikidetaichiran(prefecture_code),{"prefecture_code": prefecture_code})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
