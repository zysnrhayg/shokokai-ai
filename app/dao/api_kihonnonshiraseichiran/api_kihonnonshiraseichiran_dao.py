#Dao.vm common function
from app.mapper.api_kihonnonshiraseichiran.api_kihonnonshiraseichiran_mapper import api_kihonnonshiraseichiranMapper
import utils.mysqldb_utils
import utils.date_util
 # api_kihonnonshiraseichiran

class ApiKihonnonshiraseichiranDao :

# 関数定義_SQL文_基本のお知らせ一覧
     
    def api_kihonnonshiraseichiran(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api_kihonnonshiraseichiranMapper.api_kihonnonshiraseichiran(dtoObj.role_code),{'role_code':dtoObj.role_code})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
