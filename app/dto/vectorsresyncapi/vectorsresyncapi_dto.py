from utils.base_entity import BaseEntity


class VectorsresyncapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, vectorcollectionid="", vectorcount=""):
        super().__init__(mode, actflg, triggerid, row)
        self.vectorcollectionid = vectorcollectionid
        self.vectorcount = vectorcount

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VectorsresyncapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("vectorcollectionid", ""),
            d.get("vectorcount", ""))
