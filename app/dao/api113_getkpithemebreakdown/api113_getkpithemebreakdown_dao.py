#Dao.vm common function
from app.mapper.api113_getkpithemebreakdown.api113_getkpithemebreakdown_mapper import api113_getkpithemebreakdownMapper
import utils.mysqldb_utils
import utils.date_util
 # api113_getkpithemebreakdown

class Api113GetkpithemebreakdownDao :

# 関数定義_SQL文_KPIテーマ内訳
     
    def api113_getkpithemebreakdown(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api113_getkpithemebreakdownMapper.api113_getkpithemebreakdown(dtoObj.prefecture_code,dtoObj.shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
