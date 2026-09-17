#Dao.vm common function
from app.mapper.api_genponbunshoichiran.api_genponbunshoichiran_mapper import api_genponbunshoichiranMapper
import utils.mysqldb_utils
import utils.date_util
import utils.string_util
 # api_genponbunshoichiran

class ApiGenponbunshoichiranDao :

# 関数定義_SQL文_原本文書一覧
     
    def api_genponbunshoichiran(self,dtoObj) :
        prefecture_code = utils.string_util.changeNullToBlank(getattr(dtoObj, "prefecturecode", "") or "")
        sql = api_genponbunshoichiranMapper.api_genponbunshoichiran(prefecture_code)
        params = {"prefecture_code": prefecture_code} if prefecture_code else {}
        returnVal = utils.mysqldb_utils.querySQL(sql, params)
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
