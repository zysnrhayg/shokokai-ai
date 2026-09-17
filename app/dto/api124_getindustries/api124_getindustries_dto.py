#py_entity.vm make dto templete
from utils.base_entity import BaseEntity


class Api124GetindustriesDto(BaseEntity):

    def __init__(self, mode, actflg, triggerid, row, industrycode, label, fiscalyearid):
        super().__init__(mode, actflg, triggerid, row)
        # industry_code
        self.industrycode = industrycode
        # label
        self.label = label
        # FISCAL_YEAR_ID
        self.fiscalyearid = fiscalyearid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return Api124GetindustriesDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("industrycode", ""),
            d.get("label", ""),
            d.get("fiscalyearid", ""))
