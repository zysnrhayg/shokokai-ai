from utils.base_entity import BaseEntity

class DashboardheatmapcelltoggleapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, cellkey, excluded):
        super().__init__(mode, actflg, triggerid, row)
        self.cellkey = cellkey
        self.excluded = excluded

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return DashboardheatmapcelltoggleapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("cellkey", ""),
            d.get("excluded", ""))
