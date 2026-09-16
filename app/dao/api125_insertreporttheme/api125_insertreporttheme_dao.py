#Dao.vm common function
# 報告書テーマ登録用DAO：trn_report_themeへINSERTする
from app.mapper.api125_insertreporttheme.api125_insertreporttheme_mapper import api125_insertreportthemeMapper
import utils.mysqldb_utils
import utils.date_util
 # api125_insertreporttheme

class Api125InsertreportthemeDao :

# 関数定義_SQL文_報告書テーマ登録

    def api125_insertreporttheme(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(
            api125_insertreportthemeMapper.api125_insertreporttheme(dtoObj.reportid, dtoObj.themeid),
            {'report_id': dtoObj.reportid, 'theme_id': dtoObj.themeid})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
