import threading

from flask import session

import utils.config
from app.common import monthly_api


class MonthlyinitapiService:
    def monthlyinitapi(self, monthlyinitapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            payload = monthly_api.build_init_payload(session, monthlyinitapi_dto)
            monthly_api.set_json_success(jsonObj, payload)
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_api.fail(jsonObj, "実績確認・帳票出力の初期表示に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
