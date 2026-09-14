from utils.base_entity import BaseEntity

class DashboardheatmapfilterapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, groupvalues, includeall):
        super().__init__(mode, actflg, triggerid, row)
        self.groupvalues = groupvalues
        self.includeall = includeall

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return DashboardheatmapfilterapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("groupvalues", ""),
            d.get("includeall", ""))
