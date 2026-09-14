#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api180_dashboardheatmapfilterMapper:
    def api180_dashboardheatmapfilter(group_values,include_all):
        params = ["group_values","include_all"]
        values = [group_values,include_all]
        return utils.sql_utils.formatSQL("""SELECT r.report_id , r.form_code , p.name AS prefecture_name , s.name AS shokokai_name , r.summary FROM trn_report r LEFT JOIN mst_prefecture p ON p.prefecture_code = r.prefecture_code LEFT JOIN mst_shokokai s ON s.prefecture_code = r.prefecture_code AND s.shokokai_cd = r.shokokai_cd WHERE 1=1""",params,values)
