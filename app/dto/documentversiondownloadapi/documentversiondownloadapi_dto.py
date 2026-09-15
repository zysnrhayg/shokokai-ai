from utils.base_entity import BaseEntity

class DocumentversiondownloadapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row):
        super().__init__(mode, actflg, triggerid, row)

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = DocumentversiondownloadapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}))
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        # ダウンロード対象の文書ID・版番号
        dto.id = row.get("id", "") or row.get("knowledge_document_id", "") or row.get("knowledgedocumentid", "")
        dto.version = row.get("version", "") or row.get("version_number", "")
        return dto
