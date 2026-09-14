#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api102_getshokokaiMapper:
    def api102_getshokokai(prefecture_code,only_federation,exclude_federation):
        params = ["prefecture_code","only_federation","exclude_federation"]
        values = [prefecture_code,only_federation,exclude_federation]
        return utils.sql_utils.formatSQL("""SELECT a.:prefecturecode , a.shokokai_cd , a.name FROM mst_shokokai a JOIN mst_prefecture p ON p.prefecture_code = a.prefecture_code WHERE (NULLIF(prefecture_code , '' ) IS NULL OR a.prefecture_code = prefecture_code ) AND (NULLIF(:onlyfederation , '' ) IS NULL OR a.shokokai_cd = only_federation ) AND (NULLIF(:excludefederation , '' ) IS NULL OR a.shokokai_cd <> exclude_federation ) ORDER BY p.sort_order , a.sort_order""",params,values)
