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
