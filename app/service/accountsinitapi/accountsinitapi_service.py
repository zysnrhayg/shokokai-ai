#BasicService.vm
#make Service templete
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dao.api102_getshokokai.api102_getshokokai_dao import Api102GetshokokaiDao
from app.dao.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_dao import ApiIchiranteburushiborikomiDao
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto
from app.dto.api102_getshokokai.api102_getshokokai_dto import Api102GetshokokaiDto
from app.dto.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_dto import ApiIchiranteburushiborikomiDto
from app.common.account_list_row import account_row_to_selmap
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

    # アカウント一覧画面初期表示（絞込選択肢 + 初期一覧）
    def accountsinitapi(self, accountsinitapi_dto, jsonObj):
        PREFECTURE_CODE = utils.string_util.changeNullToBlank(accountsinitapi_dto.prefecturecode)
        SHOKOKAI_CD = utils.string_util.changeNullToBlank(accountsinitapi_dto.shokokaicd)
        ONLY_FEDERATION = utils.string_util.changeNullToBlank(accountsinitapi_dto.onlyfederation)
        EXCLUDE_FEDERATION = utils.string_util.changeNullToBlank(accountsinitapi_dto.excludefederation)

        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
        try:
            if not PREFECTURE_CODE:
                PREFECTURE_CODE = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
            # 商工会ロールで未指定なら session の組織に限定
            if not SHOKOKAI_CD:
                role = utils.string_util.changeNullToBlank(accountsinitapi_dto.rolecode)
                if role == "shokokai":
                    SHOKOKAI_CD = utils.string_util.changeNullToBlank(session.get("SHOKOKAI_CD"))

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

            # 商工会選択肢
            api102 = Api102GetshokokaiDto.dict_to_json({})
            api102.prefecturecode = PREFECTURE_CODE
            api102.onlyfederation = ONLY_FEDERATION
            api102.excludefederation = EXCLUDE_FEDERATION
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

            # 初期一覧（県で絞り、商工会指定時のみさらに絞る）
            api_list = ApiIchiranteburushiborikomiDto.dict_to_json({})
            api_list.mstuseraccountprefecturecode = PREFECTURE_CODE
            api_list.mstuseraccountshokokaicd = SHOKOKAI_CD
            api_list.limit = ""
            api_list.offset = ""
            list_rows = ApiIchiranteburushiborikomiDao().api_ichiranteburushiborikomi(api_list)
            if list_rows is not None and hasattr(list_rows, "fetchall"):
                list_rows = list_rows.fetchall()
            map_list = []
            if list_rows:
                for entity in list_rows:
                    map_list.append(account_row_to_selmap(entity))
            jsonObj.setHtml("dragB", json.dumps(map_list, ensure_ascii=False))
            jsonObj.setValue("prefecturecode", PREFECTURE_CODE)
            jsonObj.setValue("shokokaicd", SHOKOKAI_CD)
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
        except Exception as e:
            utils.config.global_log.error(e)
            jsonObj.setValue(utils.json_constant.JSONID_ERR, "アカウント一覧の初期表示に失敗しました")
            jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
            raise
        utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
