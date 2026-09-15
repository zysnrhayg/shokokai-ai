from utils.base_entity import BaseEntity


class JigyoshomeinokohokakonosodanrirekinamesapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, xx, prefecturecode, shokokaicd, limit, keyword=""):
        super().__init__(mode, actflg, triggerid, row)
        self.xx = xx
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd
        self.limit = limit
        self.keyword = keyword

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        keyword = d.get("keyword", d.get("xx", d.get("businessname", "")))
        return JigyoshomeinokohokakonosodanrirekinamesapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            keyword,
            d.get("prefecturecode", d.get("prefecture_code", "")),
            d.get("shokokaicd", d.get("shokokai_cd", "")),
            d.get("limit", "20"),
            keyword,
        )
