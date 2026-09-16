import threading

import utils.config
from app.common import reports_api


class ReportsinitapiService:
    def reportsinitapi(self, reportsinitapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            years = reports_api.fiscal_years()
            scope = reports_api.resolve_scope(reportsinitapi_dto)
            sho_pref = scope["prefecture_code"] or scope["role_prefecture_code"]
            if scope["role"] == "national" and not sho_pref:
                sho_pref = ""
            default_ym = reports_api.default_year_month(years)
            fy_id = years[0]["fiscal_year_id"] if years else ""
            jsonObj.setValue("fiscalyears", years)
            jsonObj.setValue("prefectures", reports_api.prefectures())
            jsonObj.setValue("shokokaioptions", reports_api.shokokai_options(sho_pref))
            jsonObj.setValue("forms", reports_api.report_forms(fy_id))
            jsonObj.setValue("themes", reports_api.themes())
            jsonObj.setValue("defaultyearmonth", default_ym)
            jsonObj.setValue("prefecturecode", scope["role_prefecture_code"] or scope["prefecture_code"])
            jsonObj.setValue("shokokaicd", scope["role_shokokai_cd"] or scope["shokokai_cd"])
            # 顧客設計: get_visible_reports（ロール範囲のみ）。絞込はクライアントJS
            rows = reports_api.list_visible_reports(reportsinitapi_dto)
            reports_api.set_list_result(jsonObj, rows)
        except Exception as e:
            utils.config.global_log.error(e)
            reports_api.fail(jsonObj, "報告書一覧の初期表示に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
