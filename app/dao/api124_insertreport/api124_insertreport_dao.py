#Dao.vm common function
# 報告書登録用DAO：trn_reportへINSERTする
from app.mapper.api124_insertreport.api124_insertreport_mapper import api124_insertreportMapper
import utils.mysqldb_utils
import utils.date_util
 # api124_insertreport

class Api124InsertreportDao :

# 関数定義_SQL文_報告書登録

    def api124_insertreport(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(
            api124_insertreportMapper.api124_insertreport(
                dtoObj.reportcode, dtoObj.formcode, dtoObj.fiscalyearid,
                dtoObj.prefecturecode, dtoObj.shokokaicd, dtoObj.themeid,
                dtoObj.industry, dtoObj.reportdate, dtoObj.summary, dtoObj.content,
                dtoObj.timestart, dtoObj.timeend, dtoObj.businessperson,
                dtoObj.businessname, dtoObj.staffmainname, dtoObj.staffsubname,
                dtoObj.status),
            {'report_code': dtoObj.reportcode, 'form_code': dtoObj.formcode,
             'fiscal_year_id': dtoObj.fiscalyearid, 'prefecture_code': dtoObj.prefecturecode,
             'shokokai_cd': dtoObj.shokokaicd, 'theme_id': dtoObj.themeid,
             'industry': dtoObj.industry, 'report_date': dtoObj.reportdate,
             'summary': dtoObj.summary, 'content': dtoObj.content,
             'time_start': dtoObj.timestart, 'time_end': dtoObj.timeend,
             'business_person': dtoObj.businessperson, 'business_name': dtoObj.businessname,
             'staff_main_name': dtoObj.staffmainname, 'staff_sub_name': dtoObj.staffsubname,
             'status': dtoObj.status})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
