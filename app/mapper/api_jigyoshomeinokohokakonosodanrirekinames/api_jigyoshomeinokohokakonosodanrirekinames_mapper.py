import utils.sql_utils


class api_jigyoshomeinokohokakonosodanrirekinamesMapper:
    def api_jigyoshomeinokohokakonosodanrirekinames(prefecture_code, shokokai_cd, limit, keyword=""):
        params = ["prefecture_code", "shokokai_cd", "limit", "keyword"]
        values = [prefecture_code, shokokai_cd, limit, keyword]
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
  AND business_name ILIKE :keyword
GROUP BY business_name
ORDER BY last_report_date DESC NULLS LAST
LIMIT CAST(COALESCE(NULLIF(:limit, ''), '20') AS integer)""",
            params,
            values,
        )
