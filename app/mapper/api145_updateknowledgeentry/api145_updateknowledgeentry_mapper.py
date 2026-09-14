#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api145_updateknowledgeentryMapper:
    def api145_updateknowledgeentry(title,prefecture_code,theme,knowledge_document_id,status,body,updated_by,knowledge_entry_id):
        params = ["title","prefecture_code","theme","knowledge_document_id","status","body","updated_by","knowledge_entry_id"]
        values = [title,prefecture_code,theme,knowledge_document_id,status,body,updated_by,knowledge_entry_id]
        return utils.sql_utils.formatSQL("""UPDATE trn_knowledge_entry SET :title = %s , :prefecturecode = %s , :theme = %s , :knowledgedocumentid = %s , :status = %s , :body = %s , updated_at = TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , :updatedby = %s WHERE :knowledgeentryid = %s;""",params,values)
