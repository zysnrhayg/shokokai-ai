#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api167_chatbotMapper:
    def api167_chatbot(message):
        params = ["message"]
        values = [message]
        return utils.sql_utils.formatSQL("""SELECT 1 AS result""",params,values)
