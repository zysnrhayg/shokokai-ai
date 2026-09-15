from utils.base_entity import BaseEntity


class AiproposalinitapiDto(BaseEntity):
    def __init__(
        self,
        mode,
        actflg,
        triggerid,
        row,
        knowledgeentryid,
        title,
        content,
        themelabel,
        documentversion,
        fiscalyearid,
        prefecturecode="",
    ):
        super().__init__(mode, actflg, triggerid, row)
        self.knowledgeentryid = knowledgeentryid
        self.title = title
        self.content = content
        self.themelabel = themelabel
        self.documentversion = documentversion
        self.fiscalyearid = fiscalyearid
        self.prefecturecode = prefecturecode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AiproposalinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("knowledgeentryid", d.get("knowledge_entry_id", "")),
            d.get("title", ""),
            d.get("content", ""),
            d.get("themelabel", d.get("theme_label", "")),
            d.get("documentversion", d.get("document_version", "")),
            d.get("fiscalyearid", d.get("fiscal_year_id", "")),
            d.get("prefecturecode", d.get("prefecture_code", "")),
        )
