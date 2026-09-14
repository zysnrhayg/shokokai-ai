from utils.base_entity import BaseEntity

class ReportdetailinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, reportid):
        super().__init__(mode, actflg, triggerid, row)
        self.reportid = reportid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return ReportdetailinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("reportid", ""))
