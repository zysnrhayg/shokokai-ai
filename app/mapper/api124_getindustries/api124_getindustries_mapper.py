#Mapper.vm common function mapper
# 傾聴内容変換AI画面初期表示用：業種一覧取得
# テーブル：mst_industry（論理削除考慮）
import utils.sql_utils

class api124_getindustriesMapper:
    def api124_getindustries(fiscalyearid):
        params = ["fiscalyearid"]
        values = [fiscalyearid]
        # バインド名はDAO側のキー（fiscalyearid）と一致させること
        return utils.sql_utils.formatSQL("""SELECT industry_code , label FROM mst_industry WHERE :fiscalyearid = fiscal_year_id AND deleted_at IS NULL ORDER BY sort_order""",params,values)
