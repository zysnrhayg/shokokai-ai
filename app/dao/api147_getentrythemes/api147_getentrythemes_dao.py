#Dao.vm common function
from app.mapper.api147_getentrythemes.api147_getentrythemes_mapper import api147_getentrythemesMapper
import utils.mysqldb_utils
import utils.date_util
 # api147_getentrythemes

class Api147GetentrythemesDao :

# 関数定義_SQL文_知識データテーマ
     
    def api147_getentrythemes(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api147_getentrythemesMapper.api147_getentrythemes(dtoObj.knowledge_entry_id),{'knowledge_entry_id':dtoObj.knowledge_entry_id})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
