import utils.sql_utils


class api154_getpublishedentriesMapper:
    def api154_getpublishedentries(keyword, prefecture_code):
        params = ["keyword", "prefecture_code"]
        values = [keyword, prefecture_code]
        return utils.sql_utils.formatSQL(
            """SELECT knowledge_entry_id
     , knowledge_code
     , title
     , content
     , updated_date
     , knowledge_document_id
     , prefecture_code
     , COALESCE ( ( SELECT json_agg ( json_build_object ( 'theme_id' , t.theme_id , 'label' , t.label , 'badge_class' , t.badge_class ) ORDER BY t.group_order , t.theme_id ) FROM trn_knowledge_entry_theme et JOIN mst_theme t ON t.theme_id = et.theme_id WHERE et.knowledge_entry_id = trn_knowledge_entry.knowledge_entry_id ) , '[]' ) AS theme_badges
FROM trn_knowledge_entry
WHERE status = '公開中'
  AND deleted_at IS NULL
<ifkeyword> AND (title ILIKE '%' || :keyword || '%' OR content ILIKE '%' || :keyword || '%') </ifkeyword>
<ifprefecture_code> AND (prefecture_code IS NULL OR prefecture_code = :prefecture_code) </ifprefecture_code>
ORDER BY knowledge_entry_id DESC
LIMIT 50""",
            params,
            values,
        )
