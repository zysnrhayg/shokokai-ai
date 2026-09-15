from utils.base_entity import BaseEntity

class KnowledgesearchapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, keyword):
        super().__init__(mode, actflg, triggerid, row)
        self.keyword = keyword

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return KnowledgesearchapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("keyword", ""))
