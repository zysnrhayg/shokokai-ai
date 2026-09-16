import utils.config
import threading
import utils.json_constant
from app.ai_proposal.routes import show
import utils.string_util


class AiproposalinitapiService:

    def aiproposalinitapi(self, aiproposalinitapi_dto, jsonObj):
        FISCAL_YEAR_ID = aiproposalinitapi_dto.fiscalyearid
        prefecture_code = utils.string_util.changeNullToBlank(
            getattr(aiproposalinitapi_dto, "prefecturecode", "") or ""
        )
        page_mode = str(
            utils.string_util.changeNullToBlank(
                getattr(aiproposalinitapi_dto, "pagemode", "") or ""
            )
            or ""
        ).strip().lower()
        mode = "search" if page_mode == "search" else "ai"
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            payload = show(
                mode=mode,
                prefecture_code=prefecture_code,
                fiscal_year_id=FISCAL_YEAR_ID,
            )
            jsonObj.setValue("entries", payload.get("entries") or [])
            if mode != "search":
                jsonObj.setValue("themes", payload.get("themes") or [])
                jsonObj.setValue("industries", payload.get("industries") or [])
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "初期表示に失敗しました")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
