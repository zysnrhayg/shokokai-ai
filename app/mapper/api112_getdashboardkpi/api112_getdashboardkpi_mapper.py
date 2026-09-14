#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api112_getdashboardkpiMapper:
    def api112_getdashboardkpi(prefecture_code,shokokai_cd):
        params = ["prefecture_code","shokokai_cd"]
        values = [prefecture_code,shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT fiscal_year_id , COALESCE(SUM(support_count ) , 0 ) AS support_count , COALESCE(SUM(ai_activity_count ) , 0 ) AS ai_activity_count FROM trn_kpi_daily WHERE trn_kpi_daily.:prefecturecode = prefecture_code AND trn_kpi_daily.:shokokaicd = shokokai_cd AND trn_kpi_daily.target_prefecture_code IS NULL AND trn_kpi_daily.target_shokokai_cd IS NULL GROUP BY fiscal_year_id;""",params,values)
