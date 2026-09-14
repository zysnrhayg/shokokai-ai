from utils.base_entity import BaseEntity

class KnowledgesearchapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, knowledgeentryid, title, content, themelabel, documentversion):
        super().__init__(mode, actflg, triggerid, row)
        self.knowledgeentryid = knowledgeentryid
        self.title = title
        self.content = content
        self.themelabel = themelabel
        self.documentversion = documentversion

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return KnowledgesearchapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("knowledgeentryid", ""),
            d.get("title", ""),
            d.get("content", ""),
            d.get("themelabel", ""),
            d.get("documentversion", ""))
