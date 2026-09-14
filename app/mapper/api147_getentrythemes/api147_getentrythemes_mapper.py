#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api147_getentrythemesMapper:
    def api147_getentrythemes(knowledge_entry_id):
        params = ["knowledge_entry_id"]
        values = [knowledge_entry_id]
        return utils.sql_utils.formatSQL("""SELECT t.theme_id , t.theme_code , t.label FROM trn_knowledge_entry_theme et JOIN mst_theme t ON t.theme_id = et.theme_id WHERE et.:knowledgeentryid = knowledge_entry_id;""",params,values)
