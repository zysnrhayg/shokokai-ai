#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api184_dashboardheatmappageMapper:
    def api184_dashboardheatmappage(page,page_size,role_code,fiscal_year_code,excluded_keys):
        params = ["page","page_size","role_code","fiscal_year_code","excluded_keys"]
        values = [page,page_size,role_code,fiscal_year_code,excluded_keys]
        return utils.sql_utils.formatSQL("""SELECT :fiscalyearcode , total_support_count , ai_proposal_count FROM trn_kpi_daily WHERE target_prefecture_code IS NULL AND target_shokokai_cd IS NULL""",params,values)
