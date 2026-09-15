import utils.sql_utils


class api116_getrecentreportsMapper:
    def api116_getrecentreports(prefecture_code, shokokai_cd):
        params = ["prefecture_code", "shokokai_cd"]
        values = [prefecture_code, shokokai_cd]
        return utils.sql_utils.formatSQL(
            """SELECT r.report_id
     , r.report_date
     , r.form_code
     , r.business_name
     , COALESCE(
         NULLIF(r.summary, ''),
         LEFT(COALESCE(r.content, ''), 80),
         LEFT(COALESCE(r.support_content, ''), 80),
         ''
       ) AS content_text
     , r.staff_main_name
     , r.staff_sub_name
     , r.time_start
     , r.time_end
     , r.status
     , t.label AS theme_label
     , COALESCE(f.short_label, r.form_code, '未設定') AS form_label
     , COALESCE(f.badge_class, '#1a6fa8') AS badge_class
FROM trn_report r
LEFT JOIN mst_theme t ON t.theme_id = r.theme_id
LEFT JOIN mst_form f ON f.form_code = r.form_code AND f.fiscal_year_id = r.fiscal_year_id
WHERE r.prefecture_code = :prefecture_code
  AND r.shokokai_cd = :shokokai_cd
  AND r.deleted_at IS NULL
  AND r.status != '削除'
  AND r.form_code IS NOT NULL
ORDER BY r.report_date DESC NULLS LAST, r.report_id DESC
LIMIT 4""",
            params,
            values,
        )
