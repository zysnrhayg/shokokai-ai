#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class getthemegroupsMapper:
    def getthemegroups():
        params = []
        values = []
        return utils.sql_utils.formatSQL("""SELECT t.filter_group AS filter_group , t.filter_group_label AS filter_group_label FROM ( SELECT '' AS filter_group , '全テーマ' AS filter_group_label , 0 AS sort_no UNION ALL SELECT mst_theme.filter_group AS filter_group , mst_theme.filter_group AS filter_group_label , MIN(mst_theme.group_order ) AS sort_no FROM mst_theme GROUP BY mst_theme.filter_group ) t ORDER BY t.sort_no , t.filter_group;""",params,values)
