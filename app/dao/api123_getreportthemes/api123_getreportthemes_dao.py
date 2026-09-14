#Dao.vm common function
from app.mapper.api123_getreportthemes.api123_getreportthemes_mapper import api123_getreportthemesMapper
import utils.mysqldb_utils
import utils.date_util
 # api123_getreportthemes

class Api123GetreportthemesDao :

# 関数定義_SQL文_報告書テーマ
     
    def api123_getreportthemes(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api123_getreportthemesMapper.api123_getreportthemes(dtoObj.report_id),{'report_id':dtoObj.report_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
