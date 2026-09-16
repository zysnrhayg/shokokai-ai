import threading

from flask import session

import utils.config
from app.common import monthly_api


class MonthlycsvexportapiService:
    def monthlycsvexportapi(self, monthlycsvexportapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows, filename = monthly_api.build_list_csv(session, monthlycsvexportapi_dto)
            monthly_api.set_csv_result(jsonObj, rows, filename)
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_api.fail(jsonObj, "一覧CSV出力に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
