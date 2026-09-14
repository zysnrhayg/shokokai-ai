from utils.base_entity import BaseEntity

class FormexportapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, formcode="", report_id=""):
        super().__init__(mode, actflg, triggerid, row)
        self.formcode = formcode
        self.report_id = report_id

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return FormexportapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("formcode", ""),
            d.get("report_id", ""))
