#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api144_insertknowledgeentryMapper:
    def api144_insertknowledgeentry(knowledge_entry_id,knowledge_code,title,prefecture_code,theme,knowledge_document_id,status,body,created_by,updated_by):
        params = ["knowledge_entry_id","knowledge_code","title","prefecture_code","theme","knowledge_document_id","status","body","created_by","updated_by"]
        values = [knowledge_entry_id,knowledge_code,title,prefecture_code,theme,knowledge_document_id,status,body,created_by,updated_by]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_knowledge_entry ( :knowledgeentryid , :knowledgecode , :title , :prefecturecode , :theme , :knowledgedocumentid , :status , :body , created_at , :createdby , updated_at , :updatedby ) VALUES ( %s , %s , %s , %s , %s , %s , %s , %s , TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , %s , TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , %s ) ;""",params,values)
