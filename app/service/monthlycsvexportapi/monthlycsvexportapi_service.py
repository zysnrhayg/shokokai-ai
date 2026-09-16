import threading

from flask import session

import utils.config
from app.monthly import services as monthly_services


class MonthlycsvexportapiService:
    def monthlycsvexportapi(self, monthlycsvexportapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows, filename = monthly_services.build_list_csv(session, monthlycsvexportapi_dto)
            monthly_services.set_csv_result(jsonObj, rows, filename)
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_services.fail(jsonObj, "一覧CSV出力に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
