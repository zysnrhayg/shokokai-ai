#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api145_updateknowledgeentryMapper:
    def api145_updateknowledgeentry(title,prefecturecode,knowledgedocumentid,status,content,updatedby,knowledgeentryid):
        params = ["title","prefecturecode","knowledgedocumentid","status","content","updatedby","knowledgeentryid"]
        values = [title,prefecturecode,knowledgedocumentid,status,content,updatedby,knowledgeentryid]
        # 知識データを更新する（本文はcontentカラム、更新日は当日を設定する）
        return utils.sql_utils.formatSQL("""UPDATE trn_knowledge_entry SET title = :title , prefecture_code = :prefecturecode , knowledge_document_id = :knowledgedocumentid , status = :status , content = :content , updated_date = CURRENT_DATE , updated_at = TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , updated_by = :updatedby WHERE knowledge_entry_id = :knowledgeentryid;""",params,values)
