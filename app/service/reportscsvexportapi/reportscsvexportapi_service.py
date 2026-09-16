import threading
import utils.config
from app.common import reports_api


class ReportscsvexportapiService:
    def reportscsvexportapi(self, reportscsvexportapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows = reports_api.fetch_reports(reportscsvexportapi_dto)
            marked = reports_api.mark_reports_printed(rows)
            reports_api.set_list_result(jsonObj, rows)
            jsonObj.setValue("filename", "報告書を見る.csv")
            jsonObj.setValue("markedprinted", marked)
        except Exception as e:
            utils.config.global_log.error(e)
            reports_api.fail(jsonObj, "報告書CSV出力に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
