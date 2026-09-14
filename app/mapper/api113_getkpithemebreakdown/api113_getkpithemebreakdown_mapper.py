#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api113_getkpithemebreakdownMapper:
    def api113_getkpithemebreakdown(prefecture_code,shokokai_cd):
        params = ["prefecture_code","shokokai_cd"]
        values = [prefecture_code,shokokai_cd]
        return utils.sql_utils.formatSQL("""SELECT b.fiscal_year_id , t.theme_code , t.label , t.badge_class , b.support_count FROM trn_kpi_theme_breakdown b JOIN mst_theme t ON t.theme_id = b.theme_id WHERE b.:prefecturecode = prefecture_code AND b.:shokokaicd = shokokai_cd ORDER BY b.fiscal_year_id , t.group_order;""",params,values)
