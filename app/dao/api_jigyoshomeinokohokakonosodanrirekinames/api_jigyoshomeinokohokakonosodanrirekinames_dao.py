from app.mapper.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_mapper import (
    api_jigyoshomeinokohokakonosodanrirekinamesMapper,
)
import utils.mysqldb_utils


class ApiJigyoshomeinokohokakonosodanrirekinamesDao:

    def api_jigyoshomeinokohokakonosodanrirekinames(self, dtoObj):
        prefecture_code = getattr(dtoObj, "prefecturecode", None) or ""
        shokokai_cd = getattr(dtoObj, "shokokaicd", None) or ""
        keyword = (
            getattr(dtoObj, "keyword", None)
            or getattr(dtoObj, "businessname", None)
            or getattr(dtoObj, "xx", None)
            or ""
        )
        limit = getattr(dtoObj, "limit", None) or "20"
        returnVal = utils.mysqldb_utils.querySQL(
            api_jigyoshomeinokohokakonosodanrirekinamesMapper.api_jigyoshomeinokohokakonosodanrirekinames(
                prefecture_code, shokokai_cd, keyword, limit
            ),
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "keyword": keyword,
                "limit": str(limit),
            },
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
