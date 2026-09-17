from app.mapper.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_mapper import (
    api_jigyoshomeinokohokakonosodanrirekinamesMapper,
)
import utils.mysqldb_utils


class ApiJigyoshomeinokohokakonosodanrirekinamesDao:

    def api_jigyoshomeinokohokakonosodanrirekinames(self, dtoObj):
        # 都道府県コード・商工会コード・取得件数（limit）・検索キーワードをパラメータとして使用する
        prefecture_code = getattr(dtoObj, "prefecturecode", None) or ""
        shokokai_cd = getattr(dtoObj, "shokokaicd", None) or ""
        limit = getattr(dtoObj, "limit", None) or "20"
        keyword = getattr(dtoObj, "keyword", None) or ""
        returnVal = utils.mysqldb_utils.querySQL(
            api_jigyoshomeinokohokakonosodanrirekinamesMapper.api_jigyoshomeinokohokakonosodanrirekinames(
                prefecture_code, shokokai_cd, limit, keyword
            ),
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "limit": str(limit),
                "keyword": keyword,
            },
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
