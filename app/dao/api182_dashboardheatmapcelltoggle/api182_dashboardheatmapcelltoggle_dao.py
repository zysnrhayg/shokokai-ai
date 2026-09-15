#Dao.vm common function
from app.mapper.api182_dashboardheatmapcelltoggle.api182_dashboardheatmapcelltoggle_mapper import api182_dashboardheatmapcelltoggleMapper
import utils.mysqldb_utils
import utils.date_util
 # api182_dashboardheatmapcelltoggle

class Api182DashboardheatmapcelltoggleDao :

# 関数定義_SQL文_DashboardHeatm2
     
    def api182_dashboardheatmapcelltoggle(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api182_dashboardheatmapcelltoggleMapper.api182_dashboardheatmapcelltoggle(dtoObj.cellkey,dtoObj.excluded),{'cell_key':dtoObj.cellkey,'excluded':dtoObj.excluded})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
