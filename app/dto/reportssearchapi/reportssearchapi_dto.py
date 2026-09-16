from utils.base_entity import BaseEntity

class ReportssearchapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, **kwargs):
        super().__init__(mode, actflg, triggerid, row)
        self.rolecode = kwargs.get("rolecode", "")
        self.prefecturecode = kwargs.get("prefecturecode", "")
        self.shokokaicd = kwargs.get("shokokaicd", "")
        self.yearmonth = kwargs.get("yearmonth", "")
        self.fystartmonth = kwargs.get("fystartmonth", "")
        self.fyendmonth = kwargs.get("fyendmonth", "")
        self.form = kwargs.get("form", "")
        self.theme = kwargs.get("theme", "")
        self.keyword = kwargs.get("keyword", "")
        self.includedraft = kwargs.get("includedraft", "")
        self.unprintedonly = kwargs.get("unprintedonly", "")
        self.defaultform = kwargs.get("defaultform", "")

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return ReportssearchapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            rolecode=d.get("rolecode", d.get("role_code", "")),
            prefecturecode=d.get("prefecturecode", d.get("prefecture_code", "")),
            shokokaicd=d.get("shokokaicd", d.get("shokokai_cd", "")),
            yearmonth=d.get("yearmonth", d.get("year_month", "")),
            fystartmonth=d.get("fystartmonth", d.get("fy_start_month", "")),
            fyendmonth=d.get("fyendmonth", d.get("fy_end_month", "")),
            form=d.get("form", d.get("formcode", d.get("form_code", ""))),
            theme=d.get("theme", ""),
            keyword=d.get("keyword", ""),
            includedraft=d.get("includedraft", d.get("include_draft", "")),
            unprintedonly=d.get("unprintedonly", d.get("unprinted_only", "")),
            defaultform=d.get("defaultform", d.get("default_form", "")),
        )