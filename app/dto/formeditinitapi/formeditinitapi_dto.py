from utils.base_entity import BaseEntity

class FormeditinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, prefecturecode, reportid):
        super().__init__(mode, actflg, triggerid, row)
        self.prefecturecode = prefecturecode
        self.reportid = reportid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return FormeditinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("prefecturecode", ""),
            d.get("reportid", ""))
