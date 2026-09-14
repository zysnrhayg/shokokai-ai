#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api115_getheatmapshokokaiMapper:
    def api115_getheatmapshokokai(prefecture_code,fiscal_year_id,federation_shokokai_cd):
        params = ["prefecture_code","fiscal_year_id","federation_shokokai_cd"]
        values = [prefecture_code,fiscal_year_id,federation_shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT s.shokokai_cd , s.name , COALESCE(SUM(d.support_count ) , 0 ) AS year_to_date_count FROM mst_shokokai s LEFT JOIN trn_kpi_daily d ON d.target_shokokai_cd = s.shokokai_cd AND d.:prefecturecode = s.prefecture_code AND d.:fiscalyearid = fiscal_year_id WHERE s.prefecture_code = prefecture_code AND s.shokokai_cd <> :federationshokokaicd GROUP BY s.shokokai_cd , s.name , s.sort_order ORDER BY s.sort_order;""",params,values)
