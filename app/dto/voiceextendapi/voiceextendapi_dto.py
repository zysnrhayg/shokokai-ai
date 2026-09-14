from utils.base_entity import BaseEntity

class VoiceextendapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row):
        super().__init__(mode, actflg, triggerid, row)

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VoiceextendapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""))

