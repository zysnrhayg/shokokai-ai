#Dao.vm common function
from app.mapper.getreportforms.getreportforms_mapper import getreportformsMapper
import utils.mysqldb_utils
import utils.date_util
 # getreportforms

class GetreportformsDao :

# 関数定義_SQL文_様式G一覧
     
    def getreportforms(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(getreportformsMapper.getreportforms(dtoObj.fiscal_year_id),{'fiscal_year_id':dtoObj.fiscal_year_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
