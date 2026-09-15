#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api144_insertknowledgeentryMapper:
    def api144_insertknowledgeentry(title,prefecturecode,knowledgedocumentid,status,content,createdby,updatedby):
        params = ["title","prefecturecode","knowledgedocumentid","status","content","createdby","updatedby"]
        values = [title,prefecturecode,knowledgedocumentid,status,content,createdby,updatedby]
        # 知識データを登録する（ナレッジコードは自動採番されたIDから「KN-XXX」形式で生成する）
        # ナレッジコード生成とINSERTをCTE+UPDATEの1文で行い、同時実行時の重複を防ぐ
        return utils.sql_utils.formatSQL("""WITH ins AS ( INSERT INTO trn_knowledge_entry ( knowledge_document_id , prefecture_code , knowledge_code , title , updated_date , status , content , created_at , created_by , updated_at , updated_by ) VALUES ( :knowledgedocumentid , :prefecturecode , 'KN-000' , :title , CURRENT_DATE , :status , :content , TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , :createdby , TO_CHAR(NOW( ) , 'YYYYMMDDHH24MISS' ) , :updatedby ) RETURNING knowledge_entry_id ) UPDATE trn_knowledge_entry e SET knowledge_code = 'KN-' || LPAD ( ins.knowledge_entry_id :: text , 3 , '0' ) FROM ins WHERE e.knowledge_entry_id = ins.knowledge_entry_id RETURNING ins.knowledge_entry_id AS knowledge_entry_id;""",params,values)
