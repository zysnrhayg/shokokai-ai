#Dao.vm common function
from app.mapper.api115_getheatmapshokokai.api115_getheatmapshokokai_mapper import api115_getheatmapshokokaiMapper
import utils.mysqldb_utils
import utils.date_util
 # api115_getheatmapshokokai

class Api115GetheatmapshokokaiDao :

# 関数定義_SQL文_ヒートマップ商工会
     
    def api115_getheatmapshokokai(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api115_getheatmapshokokaiMapper.api115_getheatmapshokokai(dtoObj.prefecture_code,dtoObj.fiscal_year_id,dtoObj.federation_shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'fiscal_year_id':dtoObj.fiscal_year_id,'federation_shokokai_cd':dtoObj.federation_shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
