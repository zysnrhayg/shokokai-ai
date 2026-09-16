import threading
import utils.config
from app.common import reports_api


class ReportdetailinitapiService:
    def reportdetailinitapi(self, reportdetailinitapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            detail = reports_api.fetch_report_detail(getattr(reportdetailinitapi_dto, "reportid", ""))
            if not detail:
                reports_api.fail(jsonObj, "報告書が見つかりません")
                jsonObj.setValue("report", {})
            else:
                jsonObj.setValue("report", detail)
                reports_api.set_list_result(jsonObj, [detail])
        except Exception as e:
            utils.config.global_log.error(e)
            reports_api.fail(jsonObj, "報告書詳細の取得に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")