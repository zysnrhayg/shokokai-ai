import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.dashboard_api import build_init_payload, org_from_session, set_json_success


def _run_dashboard_init(role_code, dto, jsonObj, err_msg):
    utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
    try:
        prefecture_code, shokokai_cd = org_from_session(session, dto)
        if role_code == "national":
            prefecture_code = prefecture_code or "00"
            if prefecture_code not in ("00",):
                prefecture_code = "00"
            shokokai_cd = shokokai_cd or "0021"
        payload = build_init_payload(role_code, prefecture_code, shokokai_cd)
        set_json_success(jsonObj, payload)
    except Exception as e:
        utils.config.global_log.error(e)
        jsonObj.setValue(utils.json_constant.JSONID_ERR, err_msg)
        jsonObj.setValue(
            utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
        )
        raise
    utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")


class DashboardnationalinitapiService:
    def dashboardnationalinitapi(self, dto, jsonObj):
        _run_dashboard_init(
            "national", dto, jsonObj, "全国連ダッシュボードの初期表示に失敗しました"
        )


class DashboardprefinitapiService:
    def dashboardprefinitapi(self, dto, jsonObj):
        _run_dashboard_init(
            "pref", dto, jsonObj, "県連ダッシュボードの初期表示に失敗しました"
        )


class DashboardshokokaiinitapiService:
    def dashboardshokokaiinitapi(self, dto, jsonObj):
        _run_dashboard_init(
            "shokokai", dto, jsonObj, "商工会ダッシュボードの初期表示に失敗しました"
        )
