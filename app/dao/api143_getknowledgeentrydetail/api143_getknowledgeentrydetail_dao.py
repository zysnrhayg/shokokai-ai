#Dao.vm common function
from app.mapper.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_mapper import api143_getknowledgeentrydetailMapper
import utils.mysqldb_utils
import utils.date_util
 # api143_getknowledgeentrydetail

class Api143GetknowledgeentrydetailDao :

# 関数定義_SQL文_知識データ詳細

    def api143_getknowledgeentrydetail(self,dtoObj) :
        # 知識データIDをDTOから取得して詳細を検索する
        returnVal = utils.mysqldb_utils.querySQL(api143_getknowledgeentrydetailMapper.api143_getknowledgeentrydetail(dtoObj.knowledgeentryid),{'knowledgeentryid':dtoObj.knowledgeentryid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
