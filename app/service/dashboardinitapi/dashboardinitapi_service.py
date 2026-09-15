import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.dashboard_api import build_init_payload, org_from_session, set_json_success
from app.dto.dashboardinitapi.dashboardinitapi_dto import DashboardinitapiDto
import utils.string_util


class DashboardinitapiService:

    def dashboardinitapi(self, dashboardinitapi_dto, jsonObj):
        ROLE_CODE = utils.string_util.changeNullToBlank(
            getattr(dashboardinitapi_dto, "rolecode", "") or "pref"
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            prefecture_code, shokokai_cd = org_from_session(session, dashboardinitapi_dto)
            if ROLE_CODE == "national":
                if not prefecture_code or prefecture_code == "01":
                    prefecture_code = "00"
                if not shokokai_cd:
                    shokokai_cd = "0021"
            payload = build_init_payload(ROLE_CODE, prefecture_code, shokokai_cd)
            set_json_success(jsonObj, payload)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ダッシュボードの初期表示に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
            )
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
