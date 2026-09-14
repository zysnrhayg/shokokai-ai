from utils.base_entity import BaseEntity

class FormeditsaveapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, reportid, formcode, reportdate, timestart, timeend, staffmaincode, staffsubcode, themecodes, industry, businessname, businessperson, content, summary, status, themeid):
        super().__init__(mode, actflg, triggerid, row)
        self.reportid = reportid
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
        self.themeid = themeid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return FormeditsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("reportid", ""),
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
            d.get("status", ""),
            d.get("themeid", ""))
