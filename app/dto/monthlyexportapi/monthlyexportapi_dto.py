from utils.base_entity import BaseEntity


class MonthlyexportapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, **kwargs):
        super().__init__(mode, actflg, triggerid, row)
        self.formcode = kwargs.get("formcode", "")
        self.fiscalyearcode = kwargs.get("fiscalyearcode", "")
        self.yearmonth = kwargs.get("yearmonth", "")
        self.rolecode = kwargs.get("rolecode", "")
        self.prefecturecode = kwargs.get("prefecturecode", "")
        self.shokokaicd = kwargs.get("shokokaicd", "")
        self.reportid = kwargs.get("reportid", "")

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return MonthlyexportapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            formcode=d.get("formcode", d.get("form_code", "")),
            fiscalyearcode=d.get("fiscalyearcode", d.get("fiscal_year_code", "")),
            yearmonth=d.get("yearmonth", d.get("year_month", "")),
            rolecode=d.get("rolecode", d.get("role_code", "")),
            prefecturecode=d.get("prefecturecode", d.get("prefecture_code", "")),
            shokokaicd=d.get("shokokaicd", d.get("shokokai_cd", "")),
            reportid=d.get("reportid", d.get("report_id", "")),
        )
