#Dao.vm common function
from app.mapper.api183_accountsfilter.api183_accountsfilter_mapper import api183_accountsfilterMapper
import utils.mysqldb_utils
import utils.date_util
 # api183_accountsfilter

class Api183AccountsfilterDao :

# 関数定義_SQL文_AccountsFilter
     
    def api183_accountsfilter(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api183_accountsfilterMapper.api183_accountsfilter(dtoObj.prefecture_code,dtoObj.shokokai_cd,dtoObj.permission_level,dtoObj.status,dtoObj.core_linked,dtoObj.keyword),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd,'permission_level':dtoObj.permission_level,'status':dtoObj.status,'core_linked':dtoObj.core_linked,'keyword':dtoObj.keyword})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
