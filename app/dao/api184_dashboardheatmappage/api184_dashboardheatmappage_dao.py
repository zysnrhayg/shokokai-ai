#Dao.vm common function
from app.mapper.api184_dashboardheatmappage.api184_dashboardheatmappage_mapper import api184_dashboardheatmappageMapper
import utils.mysqldb_utils
import utils.date_util
 # api184_dashboardheatmappage

class Api184DashboardheatmappageDao :

# 関数定義_SQL文_DashboardHeatm3
     
    def api184_dashboardheatmappage(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api184_dashboardheatmappageMapper.api184_dashboardheatmappage(dtoObj.page,dtoObj.pagesize,dtoObj.rolecode,dtoObj.fiscalyearcode,dtoObj.excludedkeys),{'page':dtoObj.page,'page_size':dtoObj.pagesize,'role_code':dtoObj.rolecode,'fiscal_year_code':dtoObj.fiscalyearcode,'excluded_keys':dtoObj.excludedkeys})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
