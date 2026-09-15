#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api137_insertknowledgedocumentMapper:
    def api137_insertknowledgedocument(knowledge_document_id,prefecture_code,document_code,title,category,format):
        params = ["knowledge_document_id","prefecture_code","document_code","title","category","format"]
        values = [knowledge_document_id,prefecture_code,document_code,title,category,format]
        # trn_knowledge_documentテーブルに新規文書を登録する
        return utils.sql_utils.formatSQL("""INSERT INTO trn_knowledge_document ( knowledge_document_id , prefecture_code , active_version_number , document_code , title , category , format , created_at , updated_at ) VALUES ( :knowledge_document_id , :prefecture_code , 1 , :document_code , :title , :category , :format , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) ) ;""",params,values)
