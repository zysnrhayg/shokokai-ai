import utils.config
import threading
import utils.json_constant
from app.common.api_json import entries_to_proposals
from app.dao.api154_getpublishedentries.api154_getpublishedentries_dao import Api154GetpublishedentriesDao
from app.dto.api154_getpublishedentries.api154_getpublishedentries_dto import Api154GetpublishedentriesDto
import utils.string_util


def _keyword_candidates(*texts):
    out = []
    for text in texts:
        text = (text or "").strip()
        if not text:
            continue
        out.append(text[:80])
        for part in text.replace("、", "・").replace(",", "・").split("・"):
            part = part.strip()
            if part and part not in out and len(part) >= 2:
                out.append(part[:40])
    out.append("")
    # preserve order, drop dups
    seen = set()
    uniq = []
    for x in out:
        if x in seen:
            continue
        seen.add(x)
        uniq.append(x)
    return uniq


def _fetch_entries(keyword):
    api154 = Api154GetpublishedentriesDto.dict_to_json({})
    api154.keyword = (keyword or "")[:80]
    api154.prefecturecode = ""
    return Api154GetpublishedentriesDao().api154_getpublishedentries(api154) or []


class AiproposalgenerateapiService:

    def aiproposalgenerateapi(self, aiproposalgenerateapi_dto, jsonObj):
        INDUSTRY = utils.string_util.changeNullToBlank(aiproposalgenerateapi_dto.industry)
        THEME_FILTER_GROUP = utils.string_util.changeNullToBlank(
            aiproposalgenerateapi_dto.themefiltergroup
        )
        CONSULTATION_SUMMARY = utils.string_util.changeNullToBlank(
            aiproposalgenerateapi_dto.consultationsummary
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            if not CONSULTATION_SUMMARY:
                jsonObj.setValue(utils.json_constant.JSONID_ERR, "相談概要が未入力です")
                jsonObj.setValue(
                    utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
                )
                return

            rows = []
            for kw in _keyword_candidates(THEME_FILTER_GROUP, CONSULTATION_SUMMARY, INDUSTRY):
                rows = _fetch_entries(kw)
                if rows and kw:
                    break
                if rows and not kw:
                    break

            proposals = entries_to_proposals(rows, limit=4, offset=0)
            jsonObj.setValue("proposals", proposals)
            jsonObj.setValue("industry", INDUSTRY)
            jsonObj.setValue("themefiltergroup", THEME_FILTER_GROUP)
            jsonObj.setValue("consultationsummary", CONSULTATION_SUMMARY)
            if proposals:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "AI提案を生成しました")
                jsonObj.setValue(
                    utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS
                )
            else:
                jsonObj.setValue(
                    utils.json_constant.JSONID_ERR, "該当するナレッジが見つかりませんでした"
                )
                jsonObj.setValue(
                    utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
                )
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "提案の生成に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
            )
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
