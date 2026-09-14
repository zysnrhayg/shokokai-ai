from utils.base_entity import BaseEntity

class DashboardheatmappageapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, page, pagesize, rolecode, fiscalyearcode, excludedkeys):
        super().__init__(mode, actflg, triggerid, row)
        self.page = page
        self.pagesize = pagesize
        self.rolecode = rolecode
        self.fiscalyearcode = fiscalyearcode
        self.excludedkeys = excludedkeys

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return DashboardheatmappageapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("page", ""),
            d.get("pagesize", ""),
            d.get("rolecode", ""),
            d.get("fiscalyearcode", ""),
            d.get("excludedkeys", ""))
