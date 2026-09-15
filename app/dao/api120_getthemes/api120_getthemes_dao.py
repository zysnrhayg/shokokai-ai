from app.mapper.api120_getthemes.api120_getthemes_mapper import api120_getthemesMapper
import utils.mysqldb_utils


class Api120GetthemesDao:

    def api120_getthemes(self, dtoObj):
        fiscal_year_id = (
            getattr(dtoObj, "fiscalyearid", None)
            or getattr(dtoObj, "fiscal_year_id", None)
            or ""
        )
        returnVal = utils.mysqldb_utils.querySQL(
            api120_getthemesMapper.api120_getthemes(fiscal_year_id),
            {"fiscal_year_id": str(fiscal_year_id) if fiscal_year_id not in (None, "") else ""},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
