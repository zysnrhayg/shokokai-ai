#Mapper.vm common function mapper
# 事業所過去相談履歴取得用
# テーブル：trn_report ＋ mst_form ＋ trn_report_theme ＋ mst_theme（論理削除考慮）
# バインド名はDAO側のキー（prefecturecode/shokokaicd/businessname/limit）と一致させること
import utils.sql_utils

class api_jigyoshomeinokohokakonosodanrirekihistoryMapper:
    def api_jigyoshomeinokohokakonosodanrirekihistory(prefecturecode,shokokaicd,businessname,limit):
        params = ["prefecturecode","shokokaicd","businessname","limit"]
        values = [prefecturecode,shokokaicd,businessname,limit]
        return utils.sql_utils.formatSQL("""SELECT trn_report.report_id
     , trn_report.report_date
     , trn_report.summary
     , mst_form.short_label AS form_short_label
     , mst_form.badge_class AS form_badge_class
     , mst_theme.label AS theme_label
FROM trn_report
JOIN mst_form ON mst_form.form_code = trn_report.form_code AND mst_form.fiscal_year_id = trn_report.fiscal_year_id AND mst_form.deleted_at IS NULL
JOIN mst_theme ON mst_theme.theme_id = trn_report.theme_id AND mst_theme.deleted_at IS NULL
WHERE trn_report.deleted_at IS NULL
  AND trn_report.status = '登録済み'
  AND trn_report.prefecture_code = :prefecturecode
  AND trn_report.shokokai_cd = :shokokaicd
  AND trn_report.business_name = :businessname
ORDER BY trn_report.report_date DESC , trn_report.registered_at DESC
LIMIT CAST(COALESCE(NULLIF(:limit, ''), '20') AS integer)""",params,values)
