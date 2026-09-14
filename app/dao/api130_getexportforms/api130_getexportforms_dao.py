#Dao.vm common function
from app.mapper.api130_getexportforms.api130_getexportforms_mapper import api130_getexportformsMapper
import utils.mysqldb_utils
import utils.date_util
 # api130_getexportforms

class Api130GetexportformsDao :

# 関数定義_SQL文_月次出力帳票
     
    def api130_getexportforms(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api130_getexportformsMapper.api130_getexportforms(dtoObj.fiscal_year_id),{'fiscal_year_id':dtoObj.fiscal_year_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
