import threading
import utils.config
from app.common import reports_api


class ReportssearchapiService:
    def reportssearchapi(self, reportssearchapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows = reports_api.fetch_reports(reportssearchapi_dto)
            reports_api.set_list_result(jsonObj, rows)
        except Exception as e:
            utils.config.global_log.error(e)
            reports_api.fail(jsonObj, "報告書一覧の検索に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")