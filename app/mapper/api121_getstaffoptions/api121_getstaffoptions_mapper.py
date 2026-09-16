#Mapper.vm common function mapper
# 傾聴内容変換AI画面初期表示用：担当者選択肢一覧取得
# テーブル：mst_user_account（論理削除考慮）
import utils.sql_utils

class api121_getstaffoptionsMapper:
    def api121_getstaffoptions(prefecturecode,shokokaicd):
        params = ["prefecturecode","shokokaicd"]
        values = [prefecturecode,shokokaicd]
        # バインド名はDAO側のキー（prefecturecode/shokokaicd）と一致させること
        return utils.sql_utils.formatSQL("""SELECT user_id , shokuin_kj FROM mst_user_account WHERE :prefecturecode = prefecture_code AND :shokokaicd = shokokai_cd AND deleted_at IS NULL ORDER BY shokuin_kj""",params,values)
