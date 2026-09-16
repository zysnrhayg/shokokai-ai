#Dao.vm common function
# 事業所過去相談履歴取得DAO
# バインドキーはマッパー内のバインド名（prefecturecode/shokokaicd/businessname/limit）と一致させること
# DTOはcamelCase（trnreportprefecturecode等）で受け取ること（プロジェクト規約）
from app.mapper.api_jigyoshomeinokohokakonosodanrirekihistory.api_jigyoshomeinokohokakonosodanrirekihistory_mapper import api_jigyoshomeinokohokakonosodanrirekihistoryMapper
import utils.mysqldb_utils
import utils.date_util
 # api_jigyoshomeinokohokakonosodanrirekihistory

class ApiJigyoshomeinokohokakonosodanrirekihistoryDao :

# 関数定義_SQL文_過去の相談履歴

    def api_jigyoshomeinokohokakonosodanrirekihistory(self,dtoObj) :
        prefecturecode = getattr(dtoObj, 'trnreportprefecturecode', '')
        shokokaicd = getattr(dtoObj, 'trnreportshokokaicd', '')
        businessname = getattr(dtoObj, 'trnreportbusinessname', '')
        limit = getattr(dtoObj, 'limit', '')
        returnVal = utils.mysqldb_utils.querySQL(
            api_jigyoshomeinokohokakonosodanrirekihistoryMapper.api_jigyoshomeinokohokakonosodanrirekihistory(
                prefecturecode, shokokaicd, businessname, limit
            ),
            {
                'prefecturecode': prefecturecode,
                'shokokaicd': shokokaicd,
                'businessname': businessname,
                'limit': str(limit) if limit not in (None, '') else '20'
            })
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
