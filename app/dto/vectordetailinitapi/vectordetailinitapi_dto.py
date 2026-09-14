from utils.base_entity import BaseEntity


class VectordetailinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, vectorcollectionid=""):
        super().__init__(mode, actflg, triggerid, row)
        self.vectorcollectionid = vectorcollectionid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VectordetailinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("vectorcollectionid", ""))
