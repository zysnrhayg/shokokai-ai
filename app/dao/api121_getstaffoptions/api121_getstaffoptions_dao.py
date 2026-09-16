#Dao.vm common function
# 傾聴内容変換AI画面初期表示用：担当者選択肢一覧取得DAO
# DTOはcamelCase（prefecturecode/shokokaicd）で受け取ること（プロジェクト規約）
from app.mapper.api121_getstaffoptions.api121_getstaffoptions_mapper import api121_getstaffoptionsMapper
import utils.mysqldb_utils
import utils.date_util
 # api121_getstaffoptions

class Api121GetstaffoptionsDao :

# 関数定義_SQL文_担当者選択肢

    def api121_getstaffoptions(self,dtoObj) :
        # バインドキーとマッパー内のバインド名（:prefecturecode/:shokokaicd）を一致させる
        returnVal = utils.mysqldb_utils.querySQL(api121_getstaffoptionsMapper.api121_getstaffoptions(dtoObj.prefecturecode,dtoObj.shokokaicd),{'prefecturecode':dtoObj.prefecturecode,'shokokaicd':dtoObj.shokokaicd})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
