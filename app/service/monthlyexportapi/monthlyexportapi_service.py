import threading

from flask import session

import utils.config
from app.common import monthly_api


class MonthlyexportapiService:
    def monthlyexportapi(self, monthlyexportapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            abs_path, filename, form_code, fy_code = monthly_api.resolve_export_file(monthlyexportapi_dto)
            monthly_api.set_export_file_result(jsonObj, abs_path, filename, form_code, fy_code)
        except (FileNotFoundError, ValueError) as e:
            utils.config.global_log.error(e)
            monthly_api.fail(jsonObj, str(e) or "帳票ファイルが見つかりません")
        except Exception as e:
            utils.config.global_log.error(e)
            monthly_api.fail(jsonObj, "帳票出力に失敗しました")
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
