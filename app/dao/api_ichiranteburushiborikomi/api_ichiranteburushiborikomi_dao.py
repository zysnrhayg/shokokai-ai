#Dao.vm common function
from app.mapper.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_mapper import api_ichiranteburushiborikomiMapper
import utils.mysqldb_utils
import utils.date_util
 # api_ichiranteburushiborikomi

class ApiIchiranteburushiborikomiDao :

# 関数定義_SQL文_一覧テーブル絞込

    def api_ichiranteburushiborikomi(self,dtoObj) :
        mst_user_account_prefecture_code = getattr(dtoObj, "mstuseraccountprefecturecode", None) or getattr(dtoObj, "mst_user_account_prefecture_code", "")
        mst_user_account_shokokai_cd = getattr(dtoObj, "mstuseraccountshokokaicd", None) or getattr(dtoObj, "mst_user_account_shokokai_cd", "")
        limit = getattr(dtoObj, "limit", "")
        offset = getattr(dtoObj, "offset", "")
        returnVal = utils.mysqldb_utils.querySQL(
            api_ichiranteburushiborikomiMapper.api_ichiranteburushiborikomi(mst_user_account_prefecture_code, mst_user_account_shokokai_cd, limit, offset),
            {"mstuseraccountprefecturecode": mst_user_account_prefecture_code, "mstuseraccountshokokaicd": mst_user_account_shokokai_cd, "limit": limit, "offset": offset},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
