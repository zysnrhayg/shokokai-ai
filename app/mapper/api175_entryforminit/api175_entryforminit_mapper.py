#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api175_entryforminitMapper:
    def api175_entryforminit():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT knowledge_document_id , document_code , title , category , format , active_version_number , prefecture_code FROM public.mst_knowledge_document;""",params,values)
