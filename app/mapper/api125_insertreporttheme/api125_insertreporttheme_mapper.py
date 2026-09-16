#Mapper.vm common function mapper
# 報告書テーマ登録用マッパー：trn_report_themeへINSERTする
import utils.sql_utils

class api125_insertreportthemeMapper:
    def api125_insertreporttheme(report_id,theme_id):
        params = ["report_id","theme_id"]
        values = [report_id,theme_id]
        return utils.sql_utils.formatSQL("""INSERT INTO trn_report_theme (report_id, theme_id)
VALUES (CAST(:report_id AS integer), CAST(:theme_id AS integer))
ON CONFLICT DO NOTHING""",params,values)
