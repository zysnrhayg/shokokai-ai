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
