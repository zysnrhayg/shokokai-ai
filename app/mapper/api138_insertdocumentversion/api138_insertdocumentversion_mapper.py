#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api138_insertdocumentversionMapper:
    def api138_insertdocumentversion(knowledge_document_id,prefecture_code,document_code,title,category,format,created_by,updated_by):
        params = ["knowledge_document_id","prefecture_code","document_code","title","category","format","created_by","updated_by"]
        values = [knowledge_document_id,prefecture_code,document_code,title,category,format,created_by,updated_by]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_knowledge_document ( :knowledgedocumentid , :prefecturecode , active_version_number , :documentcode , :title , :category , :format , created_at , :createdby , updated_at , :updatedby ) VALUES ( %s , %s , 1 , %s , %s , %s , %s , TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , %s , TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , %s ) ;""",params,values)
