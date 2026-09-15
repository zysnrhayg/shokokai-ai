#Dao.vm common function
from app.mapper.api_jigyoshomeinokohokakonosodanrirekihistory.api_jigyoshomeinokohokakonosodanrirekihistory_mapper import api_jigyoshomeinokohokakonosodanrirekihistoryMapper
import utils.mysqldb_utils
import utils.date_util
 # api_jigyoshomeinokohokakonosodanrirekihistory

class ApiJigyoshomeinokohokakonosodanrirekihistoryDao :

# 関数定義_SQL文_過去の相談履歴
     
    def api_jigyoshomeinokohokakonosodanrirekihistory(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api_jigyoshomeinokohokakonosodanrirekihistoryMapper.api_jigyoshomeinokohokakonosodanrirekihistory(dtoObj.trnreportprefecturecode,dtoObj.trnreportshokokaicd,dtoObj.trnreportbusinessname,dtoObj.limit),{'trn_report_prefecture_code':dtoObj.trnreportprefecturecode,'trn_report_shokokai_cd':dtoObj.trnreportshokokaicd,'trn_report_business_name':dtoObj.trnreportbusinessname,'limit':dtoObj.limit})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
