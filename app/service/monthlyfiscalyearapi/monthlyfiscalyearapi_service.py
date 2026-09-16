import threading

from flask import session

import utils.config
from app.monthly import services as monthly_services


class MonthlyfiscalyearapiService:
    def monthlyfiscalyearapi(self, monthlyfiscalyearapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            payload = monthly_services.build_fiscal_year_payload(session, monthlyfiscalyearapi_dto)
            monthly_services.set_json_success(jsonObj, payload)
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_services.fail(jsonObj, "年度切替に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
