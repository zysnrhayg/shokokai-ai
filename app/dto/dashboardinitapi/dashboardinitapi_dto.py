from utils.base_entity import BaseEntity

class DashboardinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, rolecode="", prefecturecode="", shokokaicd=""):
        super().__init__(mode, actflg, triggerid, row)
        self.rolecode = rolecode
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return DashboardinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("rolecode", ""),
            d.get("prefecturecode") or d.get("prefecture_code", ""),
            d.get("shokokaicd") or d.get("shokokai_cd", ""),
        )
