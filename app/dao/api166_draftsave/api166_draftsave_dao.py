#Dao.vm common function
from app.mapper.api166_draftsave.api166_draftsave_mapper import api166_draftsaveMapper
import utils.mysqldb_utils
import utils.date_util
 # api166_draftsave

class Api166DraftsaveDao :

# 関数定義_SQL文_DRAFTSAVE
     
    def api166_draftsave(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api166_draftsaveMapper.api166_draftsave(dtoObj.houkokushokoumokuisshiki),{'houkokushokoumokuisshiki':dtoObj.houkokushokoumokuisshiki})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
