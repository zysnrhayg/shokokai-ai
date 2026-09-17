from utils.base_entity import BaseEntity


class KnowledgesearchapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, keyword, prefecturecode=""):
        super().__init__(mode, actflg, triggerid, row)
        self.keyword = keyword
        self.prefecturecode = prefecturecode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return KnowledgesearchapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("keyword", ""),
            d.get("prefecturecode", d.get("prefecture_code", "")),
        )
