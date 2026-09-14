import utils.sql_utils


class api_kihonnonshiraseichiranMapper:
    def api_kihonnonshiraseichiran(role_code):
        params = ["role_code"]
        values = [role_code]
        return utils.sql_utils.formatSQL(
            """SELECT content
FROM trn_notice tn
WHERE tn.role_code = :role_code
AND (tn.start_date IS NULL OR tn.start_date <= CURRENT_DATE)
AND (tn.end_date IS NULL OR tn.end_date >= CURRENT_DATE)
AND tn.deleted_at IS NULL
ORDER BY sort_order , notice_id;""",
            params,
            values,
        )
