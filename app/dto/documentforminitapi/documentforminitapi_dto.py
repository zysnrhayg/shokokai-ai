from utils.base_entity import BaseEntity

class DocumentforminitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row):
        super().__init__(mode, actflg, triggerid, row)

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = DocumentforminitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}))
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        # 編集対象の原本文書ID
        dto.id = row.get("id", "") or row.get("knowledge_document_id", "") or row.get("knowledgedocumentid", "")
        return dto
