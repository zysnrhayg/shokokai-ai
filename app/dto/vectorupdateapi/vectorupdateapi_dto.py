from utils.base_entity import BaseEntity


class VectorupdateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, vectorcollectionid="", name="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.vectorcollectionid = vectorcollectionid
        self.name = name
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VectorupdateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("vectorcollectionid", ""),
            d.get("name", ""),
            d.get("status", ""))
