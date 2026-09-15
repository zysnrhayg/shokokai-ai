from utils.base_entity import BaseEntity

class AiproposalregenerateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, reason, themefiltergroup):
        super().__init__(mode, actflg, triggerid, row)
        self.reason = reason
        self.themefiltergroup = themefiltergroup

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AiproposalregenerateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("reason", ""),
            d.get("themefiltergroup", d.get("theme_filter_group", "")))
