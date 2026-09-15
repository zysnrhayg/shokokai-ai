#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_chishikidetaichiranMapper:
    def api_chishikidetaichiran():
        params = []
        values = []
        # 知識データ一覧を取得する（テーマは中間表経由でJSON配列として集約する）
        return utils.sql_utils.formatSQL("""SELECT e.knowledge_entry_id , e.knowledge_code , e.title , e.prefecture_code , p.name AS prefecture_name , e.knowledge_document_id , d.title AS document_title , e.updated_date , e.status , e.content , COALESCE ( ( SELECT json_agg ( json_build_object ( 'theme_id' , t.theme_id , 'label' , t.label , 'badge_class' , t.badge_class ) ORDER BY t.group_order , t.theme_id ) FROM trn_knowledge_entry_theme et JOIN mst_theme t ON t.theme_id = et.theme_id WHERE et.knowledge_entry_id = e.knowledge_entry_id ) , '[]' ) AS theme_badges FROM trn_knowledge_entry e LEFT JOIN trn_knowledge_document d ON d.knowledge_document_id = e.knowledge_document_id LEFT JOIN mst_prefecture p ON p.prefecture_code = e.prefecture_code ORDER BY e.knowledge_entry_id;""",params,values)
