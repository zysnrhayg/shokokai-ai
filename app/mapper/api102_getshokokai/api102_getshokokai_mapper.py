#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api102_getshokokaiMapper:
    def api102_getshokokai(prefecture_code,only_federation,exclude_federation):
        params = ["prefecture_code","only_federation","exclude_federation"]
        values = [prefecture_code,only_federation,exclude_federation]
        return utils.sql_utils.formatSQL("""SELECT a.:prefecturecode , a.shokokai_cd , a.name FROM mst_shokokai a JOIN mst_prefecture p ON p.prefecture_code = a.prefecture_code WHERE 1 = 1 <ifprefecture_code> AND a.prefecture_code = %s < / ifprefecture_code> <if:onlyfederation> AND a.shokokai_cd = %s < / ifonly_federation> <if:excludefederation> AND a.shokokai_cd <> %s < / ifexclude_federation> ORDER BY p.sort_order , a.sort_order""",params,values)
