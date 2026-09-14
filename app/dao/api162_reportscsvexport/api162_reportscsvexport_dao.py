#Dao.vm common function
from app.mapper.api162_reportscsvexport.api162_reportscsvexport_mapper import api162_reportscsvexportMapper
import utils.mysqldb_utils
import utils.date_util
 # api162_reportscsvexport

class Api162ReportscsvexportDao :

# 関数定義_SQL文_ReportsCsvExpo
     
    def api162_reportscsvexport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api162_reportscsvexportMapper.api162_reportscsvexport(dtoObj.role_prefecture_code,dtoObj.role_shokokai_cd,dtoObj.year_month,dtoObj.fy_start_month,dtoObj.fy_end_month,dtoObj.prefecture_code,dtoObj.shokokai_cd,dtoObj.form,dtoObj.theme,dtoObj.keyword),{'role_prefecture_code':dtoObj.role_prefecture_code,'role_shokokai_cd':dtoObj.role_shokokai_cd,'year_month':dtoObj.year_month,'fy_start_month':dtoObj.fy_start_month,'fy_end_month':dtoObj.fy_end_month,'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd,'form':dtoObj.form,'theme':dtoObj.theme,'keyword':dtoObj.keyword})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
