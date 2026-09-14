#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api114_getheatmapprefectureMapper:
    def api114_getheatmapprefecture(prefecture_code,fiscal_year_id):
        params = ["prefecture_code","fiscal_year_id"]
        values = [prefecture_code,fiscal_year_id]
        return utils.sql_utils.formatSQL("""SELECT p.:prefecturecode , p.name , COALESCE(SUM(d.support_count ) , 0 ) AS year_to_date_count FROM mst_prefecture p LEFT JOIN trn_kpi_daily d ON d.target_prefecture_code = p.prefecture_code AND d.prefecture_code = prefecture_code AND d.:fiscalyearid = fiscal_year_id WHERE p.is_pseudo = FALSE GROUP BY p.prefecture_code , p.name , p.sort_order ORDER BY p.sort_order;""",params,values)
