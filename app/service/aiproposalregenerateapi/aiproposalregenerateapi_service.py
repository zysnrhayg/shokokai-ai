import utils.config
import threading
import utils.json_constant
from flask import session
from app.accounts.services import resolve_account_role
from app.common.api_json import entries_to_proposals
from app.knowledge.services import get_entries_with_themes
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
    seen = set()
    uniq = []
    for x in out:
        if x in seen:
            continue
        seen.add(x)
        uniq.append(x)
    return uniq


def _pref_filter_for_kenren():
    """顧客設計：県連ロールのみ prefecture_code で絞る。"""
    if resolve_account_role() != "pref":
        return ""
    return utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))


def _fetch_entries(keyword):
    return get_entries_with_themes(keyword=keyword, prefecture_code=_pref_filter_for_kenren())


class AiproposalregenerateapiService:

    def aiproposalregenerateapi(self, aiproposalregenerateapi_dto, jsonObj):
        REASON = utils.string_util.changeNullToBlank(aiproposalregenerateapi_dto.reason)
        THEME_FILTER_GROUP = utils.string_util.changeNullToBlank(
            aiproposalregenerateapi_dto.themefiltergroup
        )
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            rows = []
            for kw in _keyword_candidates(REASON, THEME_FILTER_GROUP):
                rows = _fetch_entries(kw)
                if rows and kw:
                    break
                if rows and not kw:
                    break

            proposals = entries_to_proposals(rows, limit=2, offset=2)
            if not proposals:
                proposals = entries_to_proposals(rows, limit=2, offset=0)

            jsonObj.setValue("proposals", proposals)
            jsonObj.setValue("reason", REASON)
            if proposals:
                jsonObj.setValue(utils.json_constant.JSONID_MSG, "別の提案を表示しました")
                jsonObj.setValue(
                    utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS
                )
            else:
                jsonObj.setValue(
                    utils.json_constant.JSONID_ERR, "代替提案が見つかりませんでした"
                )
                jsonObj.setValue(
                    utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
                )
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "提案の再生成に失敗しました")
            jsonObj.setValue(
                utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL
            )
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
