#Dao.vm common function
from app.mapper.api120_getthemes.api120_getthemes_mapper import api120_getthemesMapper
import utils.mysqldb_utils
import utils.date_util
 # api120_getthemes

class Api120GetthemesDao :

# 関数定義_SQL文_支援テーマ
     
    def api120_getthemes(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api120_getthemesMapper.api120_getthemes(dtoObj.fiscal_year_id),{'fiscal_year_id':dtoObj.fiscal_year_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
