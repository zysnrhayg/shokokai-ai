#Dao.vm common function
from app.mapper.api154_getpublishedentries.api154_getpublishedentries_mapper import api154_getpublishedentriesMapper
import utils.mysqldb_utils
import utils.date_util
 # api154_getpublishedentries

class Api154GetpublishedentriesDao :

# 関数定義_SQL文_公開知識データ
     
    def api154_getpublishedentries(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api154_getpublishedentriesMapper.api154_getpublishedentries(dtoObj.keyword,dtoObj.prefecture_code),{'keyword':dtoObj.keyword,'prefecture_code':dtoObj.prefecture_code})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
