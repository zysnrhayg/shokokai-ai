#Dao.vm common function
from app.mapper.api184_dashboardheatmappage.api184_dashboardheatmappage_mapper import api184_dashboardheatmappageMapper
import utils.mysqldb_utils
import utils.date_util
 # api184_dashboardheatmappage

class Api184DashboardheatmappageDao :

# 関数定義_SQL文_DashboardHeatm3
     
    def api184_dashboardheatmappage(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api184_dashboardheatmappageMapper.api184_dashboardheatmappage(dtoObj.page,dtoObj.page_size,dtoObj.role_code,dtoObj.fiscal_year_code,dtoObj.excluded_keys),{'page':dtoObj.page,'page_size':dtoObj.page_size,'role_code':dtoObj.role_code,'fiscal_year_code':dtoObj.fiscal_year_code,'excluded_keys':dtoObj.excluded_keys})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
