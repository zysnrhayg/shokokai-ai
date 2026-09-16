#Mapper.vm common function mapper
# 傾聴内容変換AI帳票出力用：報告書データ取得
# 画面ソースに応じてビューを切替する：
#   ai-input（相談を受ける）→ v_output_f_excel（F相談受付票専用、form_code='F'限定）
#   manual-input（報告書を作る）→ v_output_reports_csv（formcode指定時は該当様式限定）
# report_id指定時は該当報告書を、未指定時はformcode限定で最新の報告書を1件返す
import utils.sql_utils

class api204_formexportMapper:
    def api204_formexport(reportid, formcode='', source=''):
        params = ["reportid"]
        values = [reportid]
        # 画面ソースが「ai-input」の場合はF相談受付票専用ビューを使用する
        if source == 'ai-input':
            # v_output_f_excel：F相談受付票専用（form_code='F' AND status='登録済み'）
            return utils.sql_utils.formatSQL("""SELECT report_id
     , "様式"
     , "報告書番号"
     , "都道府県連"
     , "商工会"
     , "実施日"
     , "開始時刻"
     , "終了時刻"
     , "支援テーマ"
     , "業種"
     , "事業所名"
     , "担当者名"
     , "概要"
     , "内容"
     , "担当（主）"
     , "担当（副）"
FROM v_output_f_excel
WHERE 1=1
  <ifreportid> AND report_id = CAST(:reportid AS integer) </ifreportid>
ORDER BY report_id DESC
LIMIT 1""",params,values)
        else:
            # v_output_reports_csv：全様式（status='登録済み'）
            # formcode指定時は該当様式の報告書のみ取得する（report_id経由で絞り込む）
            sql = """SELECT report_id
     , prefecture_code
     , shokokai_cd
     , "様式"
     , "都道府県連"
     , "商工会"
     , "報告書番号"
     , "支援テーマ"
     , "業種"
     , "実施日"
     , "開始時刻"
     , "終了時刻"
     , "事業所名"
     , "担当者名"
     , "概要"
     , "内容"
     , "音声入力の変換結果"
     , "担当（主）"
     , "担当（副）"
     , "登録日"
FROM v_output_reports_csv
WHERE 1=1"""
            if formcode:
                sql += """ AND report_id IN (
  SELECT report_id FROM trn_report WHERE form_code = '""" + formcode.replace("'", "''") + """' AND status = '登録済み' AND deleted_at IS NULL
)"""
            sql += """
  <ifreportid> AND report_id = CAST(:reportid AS integer) </ifreportid>
ORDER BY report_id DESC
LIMIT 1"""
            return utils.sql_utils.formatSQL(sql, params, values)
