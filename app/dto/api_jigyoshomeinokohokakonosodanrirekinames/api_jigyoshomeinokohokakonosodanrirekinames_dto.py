from utils.base_entity import BaseEntity


class ApiJigyoshomeinokohokakonosodanrirekinamesDto(BaseEntity):
    def __init__(
        self,
        mode,
        actflg,
        triggerid,
        row,
        businessname,
        lastreportdate,
        prefecturecode,
        shokokaicd,
        limit,
        keyword="",
        xx="",
    ):
        super().__init__(mode, actflg, triggerid, row)
        self.businessname = businessname
        self.lastreportdate = lastreportdate
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd
        self.limit = limit
        self.keyword = keyword
        self.xx = xx

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        keyword = d.get("keyword", d.get("xx", d.get("businessname", "")))
        return ApiJigyoshomeinokohokakonosodanrirekinamesDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("businessname", ""),
            d.get("lastreportdate", ""),
            d.get("prefecturecode", ""),
            d.get("shokokaicd", ""),
            d.get("limit", ""),
            keyword,
            keyword,
        )
