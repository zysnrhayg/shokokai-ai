from app.mapper.api154_getpublishedentries.api154_getpublishedentries_mapper import (
    api154_getpublishedentriesMapper,
)
import utils.mysqldb_utils


class Api154GetpublishedentriesDao:

    def api154_getpublishedentries(self, dtoObj):
        keyword = getattr(dtoObj, "keyword", None) or ""
        prefecture_code = (
            getattr(dtoObj, "prefecturecode", None)
            or getattr(dtoObj, "prefecture_code", None)
            or ""
        )
        returnVal = utils.mysqldb_utils.querySQL(
            api154_getpublishedentriesMapper.api154_getpublishedentries(keyword, prefecture_code),
            {"keyword": keyword, "prefecture_code": prefecture_code},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)

    def api154_getentrythemecodes(self, entry_ids):
        """顧客設計 SQL②：entry_id 一覧に紐づく theme_code（＋表示用 label/badge）。"""
        ids = []
        for raw in entry_ids or []:
            try:
                ids.append(int(raw))
            except (TypeError, ValueError):
                continue
        if not ids:
            return []
        # 重複除去（順序維持）
        seen = set()
        uniq = []
        for i in ids:
            if i in seen:
                continue
            seen.add(i)
            uniq.append(i)
        csv = ",".join(str(i) for i in uniq)
        returnVal = utils.mysqldb_utils.querySQL(
            api154_getpublishedentriesMapper.api154_getentrythemecodes(csv),
            {},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
