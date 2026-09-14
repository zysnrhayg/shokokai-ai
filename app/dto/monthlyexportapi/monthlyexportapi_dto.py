from utils.base_entity import BaseEntity


class MonthlyexportapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, formcode, fiscalyearcode):
        super().__init__(mode, actflg, triggerid, row)
        self.formcode = formcode
        self.fiscalyearcode = fiscalyearcode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return MonthlyexportapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("formcode", ""),
            d.get("fiscalyearcode", ""))
