#Dao.vm common function
from app.mapper.api180_dashboardheatmapfilter.api180_dashboardheatmapfilter_mapper import api180_dashboardheatmapfilterMapper
import utils.mysqldb_utils
import utils.date_util
 # api180_dashboardheatmapfilter

class Api180DashboardheatmapfilterDao :

# 関数定義_SQL文_DashboardHeatm
     
    def api180_dashboardheatmapfilter(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api180_dashboardheatmapfilterMapper.api180_dashboardheatmapfilter(dtoObj.groupvalues,dtoObj.includeall),{'group_values':dtoObj.groupvalues,'include_all':dtoObj.includeall})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
