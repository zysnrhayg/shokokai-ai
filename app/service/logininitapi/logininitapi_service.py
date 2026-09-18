import utils.config
import threading
import utils.json_constant
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto


def _jsonable_rows(rows):
    out = []
    for rec in rows or []:
        if not isinstance(rec, dict):
            continue
        item = {}
        for key, value in rec.items():
            if hasattr(value, "isoformat"):
                item[key] = value.isoformat()
            elif value is None:
                item[key] = ""
            else:
                item[key] = value
        out.append(item)
    return out


class LogininitapiService:

    def logininitapi(self, logininitapi_dto, jsonObj):
        api100_getprefecturenames = Api100GetprefecturenamesDto.dict_to_json({})
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            prefecture_rows = Api100GetprefecturenamesDao().api100_getprefecturenames(api100_getprefecturenames)
            # ホーム／ダッシュボードと同じ get_active_notices（読取のみ・有効期間）
            from app.common.dashboard_api import fetch_notices

            notices = fetch_notices("login")

            jsonObj.setValue("prefectures", _jsonable_rows(prefecture_rows))
            jsonObj.setValue("notices", notices)
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "ログイン画面の初期化に失敗しました。")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
