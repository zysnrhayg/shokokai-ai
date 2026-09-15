import utils.sql_utils


class api_jigyoshomeinokohokakonosodanrirekinamesMapper:
    def api_jigyoshomeinokohokakonosodanrirekinames(prefecture_code, shokokai_cd, keyword, limit):
        params = ["prefecture_code", "shokokai_cd", "keyword", "limit"]
        values = [prefecture_code, shokokai_cd, keyword, limit]
        return utils.sql_utils.formatSQL(
            """SELECT business_name
     , MAX(report_date) AS last_report_date
FROM trn_report
WHERE prefecture_code = :prefecture_code
  AND shokokai_cd = :shokokai_cd
  AND status != '削除'
  AND deleted_at IS NULL
  AND business_name IS NOT NULL
  AND business_name != ''
  <ifkeyword> AND business_name ILIKE '%' || :keyword || '%' </ifkeyword>
GROUP BY business_name
ORDER BY last_report_date DESC NULLS LAST
LIMIT CAST(COALESCE(NULLIF(:limit, ''), '20') AS integer)""",
            params,
            values,
        )
