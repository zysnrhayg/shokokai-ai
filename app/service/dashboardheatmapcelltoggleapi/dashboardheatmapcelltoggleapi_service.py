import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.dashboard_api import (
    fetch_heatmap_cells,
    latest_fiscal_year_id,
    org_from_session,
    parse_excluded_keys,
    set_json_success,
)
import utils.string_util


class DashboardheatmapcelltoggleapiService:

    def dashboardheatmapcelltoggleapi(self, dashboardheatmapcelltoggleapi_dto, jsonObj):
        CELL_KEY = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmapcelltoggleapi_dto, "cellkey", "")
        )
        EXCLUDED = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmapcelltoggleapi_dto, "excluded", "")
        )
        ROLE_CODE = utils.string_util.changeNullToBlank(
            getattr(dashboardheatmapcelltoggleapi_dto, "rolecode", "") or "pref"
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            prefecture_code, shokokai_cd = org_from_session(session, dashboardheatmapcelltoggleapi_dto)
            fiscal_year_id = utils.string_util.changeNullToBlank(
                getattr(dashboardheatmapcelltoggleapi_dto, "fiscalyearid", "")
            ) or latest_fiscal_year_id(prefecture_code, shokokai_cd)
            # Touch DB heatmap master so toggle stays aligned with current org cells.
            cells = fetch_heatmap_cells(ROLE_CODE, prefecture_code, shokokai_cd, fiscal_year_id)
            valid_keys = {
                (c.get("cell_key") or c.get("name") or "") for c in cells if (c.get("cell_key") or c.get("name"))
            }
            excluded = parse_excluded_keys(
                getattr(dashboardheatmapcelltoggleapi_dto, "excludedkeys", "")
            )
            if CELL_KEY:
                if EXCLUDED in ("true", "1", "True", True):
                    excluded.add(CELL_KEY)
                else:
                    excluded.discard(CELL_KEY)
            excluded = {k for k in excluded if k in valid_keys}
            set_json_success(
                jsonObj,
                {
                    "rows": cells,
                    "excludedkeys": "\u001f".join(sorted(excluded)),
                    "cellkey": CELL_KEY,
                    "excluded": EXCLUDED,
                    "fiscalyearid": fiscal_year_id,
                },
            )
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ヒートマップセル更新に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
            )
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
