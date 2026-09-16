from utils.base_entity import BaseEntity

class FormnewsaveapiDto(BaseEntity):
    # 報告書新規画面登録用DTO
    # フィールド名はプロジェクト規約に従いcamelCaseとする
    def __init__(self, mode, actflg, triggerid, row, formcode="", reportdate="", timestart="", timeend="", staffmaincode="", staffsubcode="", themecodes="", industry="", businessname="", businessperson="", content="", summary="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.formcode = formcode
        self.reportdate = reportdate
        self.timestart = timestart
        self.timeend = timeend
        self.staffmaincode = staffmaincode
        self.staffsubcode = staffsubcode
        self.themecodes = themecodes
        self.industry = industry
        self.businessname = businessname
        self.businessperson = businessperson
        self.content = content
        self.summary = summary
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return FormnewsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("formcode", ""),
            d.get("reportdate", ""),
            d.get("timestart", ""),
            d.get("timeend", ""),
            d.get("staffmaincode", ""),
            d.get("staffsubcode", ""),
            d.get("themecodes", ""),
            d.get("industry", ""),
            d.get("businessname", ""),
            d.get("businessperson", ""),
            d.get("content", ""),
            d.get("summary", ""),
            d.get("status", "登録済み"))
