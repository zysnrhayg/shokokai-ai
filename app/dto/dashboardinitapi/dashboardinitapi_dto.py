from utils.base_entity import BaseEntity

class DashboardinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, rolecode=""):
        super().__init__(mode, actflg, triggerid, row)
        self.rolecode = rolecode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return DashboardinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("rolecode", ""))
