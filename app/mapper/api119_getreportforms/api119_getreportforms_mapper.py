#Mapper.vm common function mapper
# 傾聴内容変換AI画面初期表示用：帳票様式一覧取得
# テーブル：mst_form（論理削除考慮）
import utils.sql_utils

class api119_getreportformsMapper:
    def api119_getreportforms(fiscalyearid):
        params = ["fiscalyearid"]
        values = [fiscalyearid]
        # バインド名はDAO側のキー（fiscalyearid）と一致させること
        return utils.sql_utils.formatSQL("""SELECT form_code , full_label , short_label FROM mst_form WHERE :fiscalyearid = fiscal_year_id AND deleted_at IS NULL AND badge_class IS NOT NULL ORDER BY form_code""",params,values)
