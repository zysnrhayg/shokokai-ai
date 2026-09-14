#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api141_usedocumentversionMapper:
    def api141_usedocumentversion(version_number,knowledge_document_id):
        params = ["version_number","knowledge_document_id"]
        values = [version_number,knowledge_document_id]
        return utils.sql_utils.formatSQL("""UPDATE mst_knowledge_document SET active_:versionnumber = version_number WHERE :knowledgedocumentid = knowledge_document_id;""",params,values)
