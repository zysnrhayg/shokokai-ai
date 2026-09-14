#Dao.vm common function
from app.mapper.api114_getheatmapprefecture.api114_getheatmapprefecture_mapper import api114_getheatmapprefectureMapper
import utils.mysqldb_utils
import utils.date_util
 # api114_getheatmapprefecture

class Api114GetheatmapprefectureDao :

# 関数定義_SQL文_ヒートマップ県
     
    def api114_getheatmapprefecture(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api114_getheatmapprefectureMapper.api114_getheatmapprefecture(dtoObj.prefecture_code,dtoObj.fiscal_year_id),{'prefecture_code':dtoObj.prefecture_code,'fiscal_year_id':dtoObj.fiscal_year_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
