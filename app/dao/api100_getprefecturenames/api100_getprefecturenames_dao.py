#Dao.vm common function
from app.mapper.api100_getprefecturenames.api100_getprefecturenames_mapper import api100_getprefecturenamesMapper
import utils.mysqldb_utils
import utils.date_util
 # api100_getprefecturenames

class Api100GetprefecturenamesDao :

# 関数定義_SQL文_県名取得
     
    def api100_getprefecturenames(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api100_getprefecturenamesMapper.api100_getprefecturenames(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
