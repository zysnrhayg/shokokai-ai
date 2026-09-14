from utils.base_entity import BaseEntity

class EntrysaveapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, title="", knowledgedocumentid="", content="", themeids="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.title = title
        self.knowledgedocumentid = knowledgedocumentid
        self.content = content
        self.themeids = themeids
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return EntrysaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("title", ""),
            d.get("knowledgedocumentid", ""),
            d.get("content", ""),
            d.get("themeids", ""),
            d.get("status", ""))
