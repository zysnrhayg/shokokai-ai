#Dao.vm common function
# 傾聴内容変換AI画面初期表示用：業種一覧取得DAO
# DTOはcamelCase（fiscalyearid）で受け取ること（プロジェクト規約）
from app.mapper.api124_getindustries.api124_getindustries_mapper import api124_getindustriesMapper
import utils.mysqldb_utils
import utils.date_util
 # api124_getindustries

class Api124GetindustriesDao :

# 関数定義_SQL文_業種一覧

    def api124_getindustries(self,dtoObj) :
        # バインドキーとマッパー内のバインド名（:fiscalyearid）を一致させる
        returnVal = utils.mysqldb_utils.querySQL(api124_getindustriesMapper.api124_getindustries(dtoObj.fiscalyearid),{'fiscalyearid':dtoObj.fiscalyearid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
