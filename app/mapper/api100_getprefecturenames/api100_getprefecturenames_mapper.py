import utils.sql_utils


class api100_getprefecturenamesMapper:
    def api100_getprefecturenames():
        params = []
        values = []
        return utils.sql_utils.formatSQL(
            """SELECT prefecture_code , name , short_name , region , sort_order
FROM mst_prefecture
WHERE deleted_at IS NULL
ORDER BY sort_order , prefecture_code;""",
            params,
            values,
        )
