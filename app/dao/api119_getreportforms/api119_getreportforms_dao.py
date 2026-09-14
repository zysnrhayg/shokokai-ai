#Dao.vm common function
from app.mapper.api119_getreportforms.api119_getreportforms_mapper import api119_getreportformsMapper
import utils.mysqldb_utils
import utils.date_util
 # api119_getreportforms

class Api119GetreportformsDao :

# 関数定義_SQL文_帳票様式
     
    def api119_getreportforms(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api119_getreportformsMapper.api119_getreportforms(dtoObj.fiscal_year_id),{'fiscal_year_id':dtoObj.fiscal_year_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
