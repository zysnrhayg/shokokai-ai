from app.mapper.api116_getrecentreports.api116_getrecentreports_mapper import (
    api116_getrecentreportsMapper,
)
import utils.mysqldb_utils


class Api116GetrecentreportsDao:

    def api116_getrecentreports(self, dtoObj):
        pref = getattr(dtoObj, "prefecturecode", None) or getattr(dtoObj, "prefecture_code", "") or ""
        shokokai = getattr(dtoObj, "shokokaicd", None) or getattr(dtoObj, "shokokai_cd", "") or ""
        returnVal = utils.mysqldb_utils.querySQL(
            api116_getrecentreportsMapper.api116_getrecentreports(pref, shokokai),
            {"prefecture_code": pref, "shokokai_cd": shokokai},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
