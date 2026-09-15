from utils.base_entity import BaseEntity

class DocumentdetailinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row):
        super().__init__(mode, actflg, triggerid, row)

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = DocumentdetailinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}))
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        # 詳細表示対象の原本文書ID
        dto.knowledgedocumentid = row.get("knowledgedocumentid", "") or row.get("knowledge_document_id", "")
        return dto
