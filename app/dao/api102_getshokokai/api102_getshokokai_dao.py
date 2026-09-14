#Dao.vm common function
from app.mapper.api102_getshokokai.api102_getshokokai_mapper import api102_getshokokaiMapper
import utils.mysqldb_utils
import utils.date_util
 # api102_getshokokai

class Api102GetshokokaiDao :

# 関数定義_SQL文_商工会取得
     
    def api102_getshokokai(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api102_getshokokaiMapper.api102_getshokokai(dtoObj.prefecture_code,dtoObj.only_federation,dtoObj.exclude_federation),{'prefecture_code':dtoObj.prefecture_code,'only_federation':dtoObj.only_federation,'exclude_federation':dtoObj.exclude_federation})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
