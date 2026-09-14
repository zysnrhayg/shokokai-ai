#Dao.vm common function
from app.mapper.api116_getrecentreports.api116_getrecentreports_mapper import api116_getrecentreportsMapper
import utils.mysqldb_utils
import utils.date_util
 # api116_getrecentreports

class Api116GetrecentreportsDao :

# 関数定義_SQL文_最近の報告書
     
    def api116_getrecentreports(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api116_getrecentreportsMapper.api116_getrecentreports(dtoObj.prefecture_code,dtoObj.shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
