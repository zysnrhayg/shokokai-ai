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
     , COALESCE(mst_form.short_label, '') AS form_short_label
     , COALESCE(mst_form.badge_class, '') AS form_badge_class
     , COALESCE(th.theme_labels, '') AS theme_label
FROM trn_report
INNER JOIN mst_form ON mst_form.form_code = trn_report.form_code AND mst_form.fiscal_year_id = trn_report.fiscal_year_id AND mst_form.deleted_at IS NULL
LEFT JOIN (
    SELECT trt.report_id
         , string_agg(t.label, '、' ORDER BY t.group_order, t.theme_id) AS theme_labels
    FROM trn_report_theme trt
    INNER JOIN mst_theme t ON t.theme_id = trt.theme_id AND t.deleted_at IS NULL
    GROUP BY trt.report_id
) th ON th.report_id = trn_report.report_id
WHERE trn_report.deleted_at IS NULL
  AND trn_report.status = '登録済み'
  AND trn_report.prefecture_code = :prefecturecode
  AND trn_report.shokokai_cd = :shokokaicd
  <ifbusinessname> AND trn_report.business_name = :businessname </ifbusinessname>
ORDER BY trn_report.report_date DESC , trn_report.registered_at DESC
LIMIT CAST(COALESCE(NULLIF(:limit, ''), '20') AS integer)""",params,values)
