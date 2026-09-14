#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api121_getstaffoptionsMapper:
    def api121_getstaffoptions(prefecture_code,shokokai_cd):
        params = ["prefecture_code","shokokai_cd"]
        values = [prefecture_code,shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT user_id , shokuin_kj FROM mst_user_account WHERE :prefecturecode = prefecture_code AND :shokokaicd = shokokai_cd ORDER BY shokuin_kj""",params,values)
