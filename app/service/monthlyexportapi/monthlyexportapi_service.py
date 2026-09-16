import threading

from flask import session

import utils.config
from app.monthly import routes as monthly_routes
from app.monthly import services as monthly_services


class MonthlyexportapiService:
    def monthlyexportapi(self, monthlyexportapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            # 顧客設計: app/monthly/routes.py export_excel
            abs_path, filename, form_code, fy_code = monthly_routes.export_excel(
                session, monthlyexportapi_dto
            )
            monthly_services.set_export_file_result(jsonObj, abs_path, filename, form_code, fy_code)
        except (FileNotFoundError, ValueError) as e:
            utils.config.global_log.error(e)
            monthly_services.fail(jsonObj, str(e) or "帳票ファイルが見つかりません")
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_services.fail(jsonObj, "帳票出力に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
