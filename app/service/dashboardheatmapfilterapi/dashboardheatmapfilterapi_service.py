import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.dashboard_api import (
    apply_group_filter,
    fetch_heatmap_cells,
    latest_fiscal_year_id,
    org_from_session,
    set_json_success,
)
import utils.string_util


class DashboardheatmapfilterapiService:

    def dashboardheatmapfilterapi(self, dashboardheatmapfilterapi_dto, jsonObj):
        GROUP_VALUES = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmapfilterapi_dto, "groupvalues", "")
        )
        INCLUDE_ALL = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmapfilterapi_dto, "includeall", "")
        )
        ROLE_CODE = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmapfilterapi_dto, "rolecode", "") or "pref"
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            prefecture_code, shokokai_cd = org_from_session(session, dashboardheatmapfilterapi_dto)
            fiscal_year_id = utils.string_util.changeNullToBlank(
                getattr(dashboardheatmapfilterapi_dto, "fiscalyearid", "")
            ) or latest_fiscal_year_id(prefecture_code, shokokai_cd)
            # DB-backed heatmap rows; exclusion is computed server-side from group filter.
            cells = fetch_heatmap_cells(ROLE_CODE, prefecture_code, shokokai_cd, fiscal_year_id)
            excluded = apply_group_filter(cells, GROUP_VALUES, INCLUDE_ALL)
            set_json_success(
                jsonObj,
                {
                    "rows": cells,
                    "excludedkeys": "\u001f".join(sorted(excluded)),
                    "fiscalyearid": fiscal_year_id,
                },
            )
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ヒートマップ絞込に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
            )
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
