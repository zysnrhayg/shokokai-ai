#Dao.vm common function
from app.mapper.api108_getfiscalyears.api108_getfiscalyears_mapper import api108_getfiscalyearsMapper
import utils.mysqldb_utils
import utils.date_util
 # api108_getfiscalyears

class Api108GetfiscalyearsDao :

# 関数定義_SQL文_年度一覧
     
    def api108_getfiscalyears(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api108_getfiscalyearsMapper.api108_getfiscalyears(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
