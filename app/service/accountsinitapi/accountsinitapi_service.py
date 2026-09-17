#BasicService.vm
#make Service templete
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dao.api102_getshokokai.api102_getshokokai_dao import Api102GetshokokaiDao
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto
from app.dto.api102_getshokokai.api102_getshokokai_dto import Api102GetshokokaiDto
from app.accounts.services import get_federation_shokokai_cd, get_visible_accounts, resolve_account_role
import utils.string_util
import utils.mysqldb_utils


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


class AccountsinitapiService:

    # アカウント一覧画面初期表示（絞込選択肢 + ロール別可視一覧）
    def accountsinitapi(self, accountsinitapi_dto, jsonObj):
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            role = resolve_account_role(
                utils.string_util.changeNullToBlank(accountsinitapi_dto.rolecode)
            )
            session_pref = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
            federation_cd = get_federation_shokokai_cd()

            # 都道府県マスタ
            pref_rows = Api100GetprefecturenamesDao().api100_getprefecturenames(
                Api100GetprefecturenamesDto.dict_to_json({})
            )
            jsonObj.setValue("prefectures", _jsonable_rows(pref_rows))

            # 権限ロール（DB 実値）
            perm_rows = utils.mysqldb_utils.result_to_list_of_dict(
                utils.mysqldb_utils.querySQL(
                    """
SELECT DISTINCT permission_level
FROM mst_user_account
WHERE deleted_at IS NULL
  AND permission_level IS NOT NULL
  AND permission_level <> ''
ORDER BY permission_level
""",
                    {},
                )
            )
            permission_levels = [
                utils.string_util.changeNullToBlank(r.get("permission_level"))
                for r in (perm_rows or [])
                if r.get("permission_level")
            ]
            if not permission_levels:
                permission_levels = ["管理者", "一般職員"]
            jsonObj.setValue("permissionlevels", permission_levels)

            # 商工会選択肢（全国=全件 / 県連=自県・県連除く / 商工会=不要だが自組織のみ）
            api102 = Api102GetshokokaiDto.dict_to_json({})
            if role == "national":
                api102.prefecturecode = ""
                api102.onlyfederation = ""
                api102.excludefederation = ""
            elif role == "pref":
                api102.prefecturecode = session_pref
                api102.onlyfederation = ""
                api102.excludefederation = federation_cd
            else:
                api102.prefecturecode = session_pref
                api102.onlyfederation = ""
                api102.excludefederation = ""
            shokokai_rows = Api102GetshokokaiDao().api102_getshokokai(api102) or []
            shokokai_opts = []
            for rec in shokokai_rows:
                if not isinstance(rec, dict):
                    continue
                shokokai_opts.append(
                    {
                        "prefecture_code": utils.string_util.changeNullToBlank(rec.get("prefecture_code")),
                        "shokokai_cd": utils.string_util.changeNullToBlank(rec.get("shokokai_cd")),
                        "name": utils.string_util.changeNullToBlank(rec.get("name")),
                    }
                )
            jsonObj.setValue("shokokaioptions", shokokai_opts)

            # 初期一覧（ロール可視範囲のみ。UI絞込は accountsfilterapi で DB 再取得）
            map_list, role, pref, sho = get_visible_accounts(
                role,
                getattr(accountsinitapi_dto, "limit", ""),
                getattr(accountsinitapi_dto, "offset", ""),
            )
            jsonObj.setHtml("dragB", json.dumps(map_list, ensure_ascii=False))
            jsonObj.setValue("rolecode", role)
            jsonObj.setValue("prefecturecode", pref)
            jsonObj.setValue("shokokaicd", sho)
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "アカウント一覧の初期表示に失敗しました")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
