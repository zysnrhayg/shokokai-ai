#Dao.vm common function
from app.mapper.api169_monthlyexport.api169_monthlyexport_mapper import api169_monthlyexportMapper
import utils.mysqldb_utils
import utils.date_util
 # api169_monthlyexport

class Api169MonthlyexportDao :

# 関数定義_SQL文_MonthlyExport
     
    def api169_monthlyexport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api169_monthlyexportMapper.api169_monthlyexport(dtoObj.form_code,dtoObj.fiscal_year_code),{'form_code':dtoObj.form_code,'fiscal_year_code':dtoObj.fiscal_year_code})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
