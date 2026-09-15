#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api139_updateknowledgedocumentMapper:
    def api139_updateknowledgedocument(title,prefecture_code,category,format,updated_by,knowledge_document_id):
        params = ["title","prefecture_code","category","format","updated_by","knowledge_document_id"]
        values = [title,prefecture_code,category,format,updated_by,knowledge_document_id]
        # 原本文書マスタを更新する（タイトル・適用範囲・カテゴリ・形式・更新日時・更新者）
        # prefecture_codeが空文字の場合はNULLに変換してCHECK約束を回避する
        return utils.sql_utils.formatSQL("""UPDATE trn_knowledge_document SET title = :title , prefecture_code = NULLIF( :prefecture_code , '' ) , category = :category , format = :format , updated_at = TO_CHAR( NOW( ) , 'YYYYMMDDHH24MISS' ) , updated_by = :updated_by WHERE knowledge_document_id = :knowledge_document_id ;""",params,values)
