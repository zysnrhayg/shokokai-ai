import utils.sql_utils


class api154_getpublishedentriesMapper:
    def api154_getpublishedentries(keyword, prefecture_code):
        """顧客設計 SQL①：ナレッジエントリー一覧（文書タイトル・県名を JOIN）。"""
        params = ["keyword", "prefecture_code"]
        values = [keyword, prefecture_code]
        return utils.sql_utils.formatSQL(
            """SELECT trn_knowledge_entry.knowledge_entry_id
     , trn_knowledge_entry.knowledge_code
     , trn_knowledge_entry.title
     , trn_knowledge_entry.content
     , trn_knowledge_entry.updated_date
     , trn_knowledge_entry.knowledge_document_id
     , trn_knowledge_entry.prefecture_code
     , trn_knowledge_document.title AS document_title
     , mst_prefecture.name AS prefecture_name
FROM trn_knowledge_entry
LEFT JOIN trn_knowledge_document
  ON trn_knowledge_document.knowledge_document_id = trn_knowledge_entry.knowledge_document_id
LEFT JOIN mst_prefecture
  ON mst_prefecture.prefecture_code = trn_knowledge_entry.prefecture_code
WHERE trn_knowledge_entry.status = '公開中'
  AND trn_knowledge_entry.deleted_at IS NULL
<ifkeyword> AND (trn_knowledge_entry.title ILIKE '%' || :keyword || '%' ESCAPE '!' OR trn_knowledge_entry.content ILIKE '%' || :keyword || '%' ESCAPE '!' OR trn_knowledge_entry.knowledge_code ILIKE '%' || :keyword || '%' ESCAPE '!' OR EXISTS ( SELECT 1 FROM trn_knowledge_entry_theme et JOIN mst_theme t ON t.theme_id = et.theme_id WHERE et.knowledge_entry_id = trn_knowledge_entry.knowledge_entry_id AND t.label ILIKE '%' || :keyword || '%' ESCAPE '!' )) </ifkeyword>
<ifprefecture_code> AND (trn_knowledge_entry.prefecture_code IS NULL OR trn_knowledge_entry.prefecture_code = :prefecture_code) </ifprefecture_code>
ORDER BY trn_knowledge_entry.knowledge_entry_id
LIMIT 50""",
            params,
            values,
        )

    def api154_getentrythemecodes(entry_ids_csv):
        """顧客設計 SQL②：各エントリの支援テーマタグ（theme_code）。entry_ids_csv は整数IDのカンマ区切り。"""
        # ID は呼び出し側で int 化済み。空のときは呼ばない。
        return (
            """SELECT trn_knowledge_entry_theme.knowledge_entry_id
     , mst_theme.theme_code
     , mst_theme.theme_id
     , mst_theme.label
     , mst_theme.badge_class
FROM trn_knowledge_entry_theme
JOIN mst_theme ON mst_theme.theme_id = trn_knowledge_entry_theme.theme_id
WHERE trn_knowledge_entry_theme.knowledge_entry_id = ANY(ARRAY["""
            + entry_ids_csv
            + """]::integer[])
ORDER BY trn_knowledge_entry_theme.knowledge_entry_id
       , mst_theme.group_order
       , mst_theme.theme_id"""
        )
