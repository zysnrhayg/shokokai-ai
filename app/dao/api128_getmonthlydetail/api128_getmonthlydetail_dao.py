#Dao.vm common function
from app.mapper.api128_getmonthlydetail.api128_getmonthlydetail_mapper import api128_getmonthlydetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api128_getmonthlydetail

class Api128GetmonthlydetailDao :

# 関数定義_SQL文_月次明細
     
    def api128_getmonthlydetail(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api128_getmonthlydetailMapper.api128_getmonthlydetail(dtoObj.prefecture_code,dtoObj.shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
