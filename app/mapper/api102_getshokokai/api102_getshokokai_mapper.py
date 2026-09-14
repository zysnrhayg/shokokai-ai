#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api102_getshokokaiMapper:
    def api102_getshokokai(prefecture_code,only_federation,exclude_federation):
        params = ["prefecture_code","only_federation","exclude_federation"]
        values = [prefecture_code,only_federation,exclude_federation]
        return utils.sql_utils.formatSQL(
            """SELECT a.prefecture_code , a.shokokai_cd , a.name
FROM mst_shokokai a
JOIN mst_prefecture p ON p.prefecture_code = a.prefecture_code
WHERE a.deleted_at IS NULL
<ifprefecture_code> AND a.prefecture_code = :prefecture_code </ifprefecture_code>
<ifonly_federation> AND a.shokokai_cd = :only_federation </ifonly_federation>
<ifexclude_federation> AND a.shokokai_cd <> :exclude_federation </ifexclude_federation>
ORDER BY p.sort_order , a.sort_order""",
            params,
            values,
        )
