import utils.sql_utils


class api120_getthemesMapper:
    def api120_getthemes(fiscal_year_id):
        params = ["fiscal_year_id"]
        values = [fiscal_year_id]
        return utils.sql_utils.formatSQL(
            """SELECT theme_id
     , theme_code
     , label
FROM mst_theme
WHERE deleted_at IS NULL
<iffiscal_year_id> AND fiscal_year_id = CAST(:fiscal_year_id AS integer) </iffiscal_year_id>
ORDER BY group_order , theme_id""",
            params,
            values,
        )
