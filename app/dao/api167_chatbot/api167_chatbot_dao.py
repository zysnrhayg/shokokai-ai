#Dao.vm common function
from app.mapper.api167_chatbot.api167_chatbot_mapper import api167_chatbotMapper
import utils.mysqldb_utils
import utils.date_util
 # api167_chatbot

class Api167ChatbotDao :

# 関数定義_SQL文_CHATBOT
     
    def api167_chatbot(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api167_chatbotMapper.api167_chatbot(dtoObj.message),{'message':dtoObj.message})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
