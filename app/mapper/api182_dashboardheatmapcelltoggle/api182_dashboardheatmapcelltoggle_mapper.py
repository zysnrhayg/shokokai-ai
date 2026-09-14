#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api182_dashboardheatmapcelltoggleMapper:
    def api182_dashboardheatmapcelltoggle(cell_key,excluded):
        params = ["cell_key","excluded"]
        values = [cell_key,excluded]
        return utils.sql_utils.formatSQL("""SELECT fiscal_year_code , total_support_count , ai_proposal_count FROM trn_kpi_daily WHERE target_prefecture_code IS NULL AND target_shokokai_cd IS NULL""",params,values)
