#Dao.vm common function
from app.mapper.api173_documentforminit.api173_documentforminit_mapper import api173_documentforminitMapper
import utils.mysqldb_utils
import utils.date_util
 # api173_documentforminit

class Api173DocumentforminitDao :

# 関数定義_SQL文_DocumentFormIn
     
    def api173_documentforminit(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api173_documentforminitMapper.api173_documentforminit(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
