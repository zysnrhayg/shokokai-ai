import threading

from flask import session

import utils.config
from app.monthly import services as monthly_services


class MonthlyinitapiService:
    def monthlyinitapi(self, monthlyinitapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            payload = monthly_services.build_init_payload(session, monthlyinitapi_dto)
            monthly_services.set_json_success(jsonObj, payload)
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_services.fail(jsonObj, "実績確認・帳票出力の初期表示に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
