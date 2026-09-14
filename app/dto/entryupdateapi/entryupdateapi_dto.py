from utils.base_entity import BaseEntity

class EntryupdateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, knowledgeentryid="", title="", knowledgedocumentid="", content="", themeids="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.knowledgeentryid = knowledgeentryid
        self.title = title
        self.knowledgedocumentid = knowledgedocumentid
        self.content = content
        self.themeids = themeids
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return EntryupdateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("knowledgeentryid", ""),
            d.get("title", ""),
            d.get("knowledgedocumentid", ""),
            d.get("content", ""),
            d.get("themeids", ""),
            d.get("status", ""))
