#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_chishikidetaichiranMapper:
    def api_chishikidetaichiran(prefecture_code):
        params = ["prefecture_code"]
        values = [prefecture_code]
        # 知識データ一覧を取得する（テーマは中間表経由でJSON配列として集約する）
        # 県連ロールの場合、全国共有（prefecture_code IS NULL）＋自県分のみに絞込
        return utils.sql_utils.formatSQL("""SELECT trn_knowledge_entry.* , trn_knowledge_document.title AS document_title , mst_prefecture.name AS prefecture_name , COALESCE ( ( SELECT json_agg ( json_build_object ( 'theme_id' , t.theme_id , 'label' , t.label , 'badge_class' , t.badge_class ) ORDER BY t.group_order , t.theme_id ) FROM trn_knowledge_entry_theme et JOIN mst_theme t ON t.theme_id = et.theme_id WHERE et.knowledge_entry_id = trn_knowledge_entry.knowledge_entry_id ) , '[]' ) AS theme_badges FROM trn_knowledge_entry LEFT JOIN trn_knowledge_document ON trn_knowledge_document.knowledge_document_id = trn_knowledge_entry.knowledge_document_id LEFT JOIN mst_prefecture ON mst_prefecture.prefecture_code = trn_knowledge_entry.prefecture_code WHERE trn_knowledge_entry.deleted_at IS NULL <ifprefecture_code> AND ( trn_knowledge_entry.prefecture_code IS NULL OR trn_knowledge_entry.prefecture_code = :prefecture_code ) </ifprefecture_code> ORDER BY trn_knowledge_entry.knowledge_entry_id""",params,values)
