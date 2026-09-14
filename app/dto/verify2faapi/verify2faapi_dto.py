from utils.base_entity import BaseEntity

class Verify2faapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, code="", rememberdevice=""):
        super().__init__(mode, actflg, triggerid, row)
        self.code = code
        self.rememberdevice = rememberdevice

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return Verify2faapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("code", ""),
            d.get("rememberdevice", ""))
