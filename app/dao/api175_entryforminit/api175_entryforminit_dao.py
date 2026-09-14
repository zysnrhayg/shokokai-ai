#Dao.vm common function
from app.mapper.api175_entryforminit.api175_entryforminit_mapper import api175_entryforminitMapper
import utils.mysqldb_utils
import utils.date_util
 # api175_entryforminit

class Api175EntryforminitDao :

# 関数定義_SQL文_EntryFormInit
     
    def api175_entryforminit(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api175_entryforminitMapper.api175_entryforminit(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
