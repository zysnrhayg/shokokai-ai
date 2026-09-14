from utils.base_entity import BaseEntity

class EntryforminitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, id=""):
        super().__init__(mode, actflg, triggerid, row)
        self.id = id

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return EntryforminitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("id", ""))
