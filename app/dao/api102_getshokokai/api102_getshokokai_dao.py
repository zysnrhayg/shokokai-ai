#Dao.vm common function
from app.mapper.api102_getshokokai.api102_getshokokai_mapper import api102_getshokokaiMapper
import utils.mysqldb_utils
import utils.date_util
 # api102_getshokokai

class Api102GetshokokaiDao :

# 関数定義_SQL文_商工会取得
     
    def api102_getshokokai(self,dtoObj) :
        prefecture_code = getattr(dtoObj, "prefecturecode", None) or getattr(dtoObj, "prefecture_code", "")
        only_federation = getattr(dtoObj, "onlyfederation", None) or getattr(dtoObj, "only_federation", "")
        exclude_federation = getattr(dtoObj, "excludefederation", None) or getattr(dtoObj, "exclude_federation", "")
        returnVal = utils.mysqldb_utils.querySQL(
            api102_getshokokaiMapper.api102_getshokokai(prefecture_code, only_federation, exclude_federation),
            {"prefecture_code": prefecture_code, "only_federation": only_federation, "exclude_federation": exclude_federation},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
