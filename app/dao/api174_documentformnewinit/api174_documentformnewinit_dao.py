#Dao.vm common function
from app.mapper.api174_documentformnewinit.api174_documentformnewinit_mapper import api174_documentformnewinitMapper
import utils.mysqldb_utils
import utils.date_util
 # api174_documentformnewinit

class Api174DocumentformnewinitDao :

# 関数定義_SQL文_DocumentFormNe
     
    def api174_documentformnewinit(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api174_documentformnewinitMapper.api174_documentformnewinit(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
