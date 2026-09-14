#Dao.vm common function
from app.mapper.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_mapper import api_jigyoshomeinokohokakonosodanrirekinamesMapper
import utils.mysqldb_utils
import utils.date_util
 # api_jigyoshomeinokohokakonosodanrirekinames

class ApiJigyoshomeinokohokakonosodanrirekinamesDao :

# 関数定義_SQL文_事業所名の候補
     
    def api_jigyoshomeinokohokakonosodanrirekinames(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api_jigyoshomeinokohokakonosodanrirekinamesMapper.api_jigyoshomeinokohokakonosodanrirekinames(dtoObj.prefecture_code,dtoObj.shokokai_cd,dtoObj.limit),{'prefecture_code':dtoObj.prefecture_code,'shokokai_cd':dtoObj.shokokai_cd,'limit':dtoObj.limit})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
