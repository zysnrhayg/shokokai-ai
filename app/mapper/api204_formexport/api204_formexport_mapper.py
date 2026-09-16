#Mapper.vm common function mapper
# 傾聴内容変換AI帳票出力用：F相談受付票データ取得
# テーブル：v_output_f_excel（ビュー）
# report_id指定時は該当報告書を、未指定時は最新の報告書を1件返す
import utils.sql_utils

class api204_formexportMapper:
    def api204_formexport(reportid):
        params = ["reportid"]
        values = [reportid]
        # ビュー「v_output_f_excel」からF相談受付票データを取得する（日文カラム名はダブルクォート必須）
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
     , "担当（主）"
     , "担当（副）"
     , "概要"
     , "内容"
FROM v_output_f_excel
WHERE 1=1
  <ifreportid> AND report_id = CAST(:reportid AS integer) </ifreportid>
ORDER BY report_id DESC
LIMIT 1""",params,values)
