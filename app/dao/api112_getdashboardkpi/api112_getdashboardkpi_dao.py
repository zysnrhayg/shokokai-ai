#Dao.vm common function
from app.mapper.api112_getdashboardkpi.api112_getdashboardkpi_mapper import api112_getdashboardkpiMapper
import utils.mysqldb_utils
import utils.date_util
 # api112_getdashboardkpi

class Api112GetdashboardkpiDao :

# 関数定義_SQL文_ダッシュボードKPI
     
    def api112_getdashboardkpi(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api112_getdashboardkpiMapper.api112_getdashboardkpi(dtoObj.prefecture_code,dtoObj.shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
