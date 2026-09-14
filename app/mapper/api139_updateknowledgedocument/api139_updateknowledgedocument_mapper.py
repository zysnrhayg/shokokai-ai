#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api139_updateknowledgedocumentMapper:
    def api139_updateknowledgedocument(title,prefecture_code,category,format,updated_by,knowledge_document_id):
        params = ["title","prefecture_code","category","format","updated_by","knowledge_document_id"]
        values = [title,prefecture_code,category,format,updated_by,knowledge_document_id]
        return utils.sql_utils.formatSQL("""UPDATE trn_knowledge_document SET :prefecturecode = %s , :title = %s , :category = %s , :format = %s , updated_at = TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , :updatedby = %s WHERE :knowledgedocumentid = %s;""",params,values)
