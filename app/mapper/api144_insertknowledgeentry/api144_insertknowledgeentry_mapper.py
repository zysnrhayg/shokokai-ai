#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api144_insertknowledgeentryMapper:
    def api144_insertknowledgeentry(title,prefecturecode,knowledgedocumentid,status,content,createdby,updatedby):
        params = ["title","prefecturecode","knowledgedocumentid","status","content","createdby","updatedby"]
        values = [title,prefecturecode,knowledgedocumentid,status,content,createdby,updatedby]
        # 知識データを登録する（ナレッジコードはMAX(id)+1から「KN-XXX」形式で生成する）
        # CTE内でMAX(id)+1を計算し、INSERT時に直接正しいナレッジコードを設定する（固定値「KN-000」による一意制約違反を回避）
        return utils.sql_utils.formatSQL("""WITH next_id AS ( SELECT COALESCE ( MAX ( knowledge_entry_id ) , 0 ) + 1 AS next_id FROM trn_knowledge_entry ) , ins AS ( INSERT INTO trn_knowledge_entry ( knowledge_document_id , prefecture_code , knowledge_code , title , updated_date , status , content , created_at , created_by , updated_at , updated_by ) SELECT :knowledgedocumentid , :prefecturecode , 'KN-' || LPAD ( next_id :: text , 3 , '0' ) , :title , CURRENT_DATE , :status , :content , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , :createdby , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , :updatedby FROM next_id RETURNING knowledge_entry_id ) SELECT ins.knowledge_entry_id FROM ins ;""",params,values)
