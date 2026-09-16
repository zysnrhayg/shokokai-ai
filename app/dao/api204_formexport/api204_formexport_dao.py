#Dao.vm common function
# 傾聴内容変換AI帳票出力用：F相談受付票データ取得DAO
# バインドキーはマッパー内のバインド名（reportid）と一致させること
from app.mapper.api204_formexport.api204_formexport_mapper import api204_formexportMapper
import utils.mysqldb_utils
import utils.date_util
 # api204_formexport

class Api204FormexportDao :

# 関数定義_SQL文_FORMEXPORT204

    def api204_formexport(self,dtoObj) :
        reportid = getattr(dtoObj, 'reportid', '')
        returnVal = utils.mysqldb_utils.querySQL(
            api204_formexportMapper.api204_formexport(reportid),
            {'reportid': reportid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
