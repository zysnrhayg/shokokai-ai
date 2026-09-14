#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api137_insertknowledgedocumentMapper:
    def api137_insertknowledgedocument(knowledge_document_id,uploaded_date,file_size_kb,status,file_path):
        params = ["knowledge_document_id","uploaded_date","file_size_kb","status","file_path"]
        values = [knowledge_document_id,uploaded_date,file_size_kb,status,file_path]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_knowledge_document_version ( :knowledgedocumentid , version_number , :uploadeddate , :filesizekb , :status , :filepath ) VALUES ( %s , 1 , %s , %s , %s , %s ) ;""",params,values)
