#Dao.vm common function
from app.mapper.api127_deletereportthemes.api127_deletereportthemes_mapper import api127_deletereportthemesMapper
import utils.mysqldb_utils
import utils.date_util
 # api127_deletereportthemes

class Api127DeletereportthemesDao :

# 関数定義_SQL文_報告書テーマ削除
     
    def api127_deletereportthemes(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api127_deletereportthemesMapper.api127_deletereportthemes(dtoObj.report_id),{'report_id':dtoObj.report_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
