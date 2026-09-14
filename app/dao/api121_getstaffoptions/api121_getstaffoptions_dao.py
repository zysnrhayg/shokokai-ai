#Dao.vm common function
from app.mapper.api121_getstaffoptions.api121_getstaffoptions_mapper import api121_getstaffoptionsMapper
import utils.mysqldb_utils
import utils.date_util
 # api121_getstaffoptions

class Api121GetstaffoptionsDao :

# 関数定義_SQL文_担当者選択肢
     
    def api121_getstaffoptions(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api121_getstaffoptionsMapper.api121_getstaffoptions(dtoObj.prefecture_code,dtoObj.shokokai_cd),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
