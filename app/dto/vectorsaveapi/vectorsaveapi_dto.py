from utils.base_entity import BaseEntity


class VectorsaveapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, name="", collectioncode=""):
        super().__init__(mode, actflg, triggerid, row)
        self.name = name
        self.collectioncode = collectioncode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VectorsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("name", ""),
            d.get("collectioncode", ""))
