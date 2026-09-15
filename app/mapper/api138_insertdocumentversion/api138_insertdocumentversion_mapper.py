#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api138_insertdocumentversionMapper:
    def api138_insertdocumentversion(knowledge_document_id,version_number,uploaded_by,file_size_kb,status,file_path):
        params = ["knowledge_document_id","version_number","uploaded_by","file_size_kb","status","file_path"]
        values = [knowledge_document_id,version_number,uploaded_by,file_size_kb,status,file_path]
        # trn_knowledge_document_versionテーブルに新規版を登録する
        return utils.sql_utils.formatSQL("""INSERT INTO trn_knowledge_document_version ( knowledge_document_id , version_number , uploaded_date , uploaded_by , file_size_kb , status , file_path , created_at , updated_at ) VALUES ( :knowledge_document_id , :version_number , CURRENT_DATE , :uploaded_by , :file_size_kb , :status , :file_path , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) ) ;""",params,values)
