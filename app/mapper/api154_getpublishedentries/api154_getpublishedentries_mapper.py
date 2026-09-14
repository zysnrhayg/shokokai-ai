#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api154_getpublishedentriesMapper:
    def api154_getpublishedentries(keyword,prefecture_code):
        params = ["keyword","prefecture_code"]
        values = [keyword,prefecture_code]
        return utils.sql_utils.formatSQL("""ORDER BY knowledge_entry_id;""",params,values)
