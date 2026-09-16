#Dao.vm common function
# 傾聴内容変換AI画面初期表示用：帳票様式一覧取得DAO
# DTOはcamelCase（fiscalyearid）で受け取ること（プロジェクト規約）
from app.mapper.api119_getreportforms.api119_getreportforms_mapper import api119_getreportformsMapper
import utils.mysqldb_utils
import utils.date_util
 # api119_getreportforms

class Api119GetreportformsDao :

# 関数定義_SQL文_帳票様式

    def api119_getreportforms(self,dtoObj) :
        # バインドキーとマッパー内のバインド名（:fiscalyearid）を一致させる
        returnVal = utils.mysqldb_utils.querySQL(api119_getreportformsMapper.api119_getreportforms(dtoObj.fiscalyearid),{'fiscalyearid':dtoObj.fiscalyearid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
