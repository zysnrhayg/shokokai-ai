from utils.base_entity import BaseEntity

class AiproposalgenerateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, industry, themefiltergroup, consultationsummary):
        super().__init__(mode, actflg, triggerid, row)
        self.industry = industry
        self.themefiltergroup = themefiltergroup
        self.consultationsummary = consultationsummary

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AiproposalgenerateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("industry", ""),
            d.get("themefiltergroup", d.get("theme_filter_group", "")),
            d.get("consultationsummary", d.get("consultation_summary", "")))
