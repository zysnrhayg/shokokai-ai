from utils.base_entity import BaseEntity

class DocumentupdateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row):
        super().__init__(mode, actflg, triggerid, row)

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = DocumentupdateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}))
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        # 文書更新APIの入力パラメータ
        dto.knowledgedocumentid = row.get("knowledgedocumentid", "") or row.get("knowledge_document_id", "")
        dto.title = row.get("title", "")
        dto.category = row.get("category", "")
        dto.format = row.get("format", "")
        dto.prefecturecode = row.get("prefecturecode", "") or row.get("prefecture_code", "")
        dto.status = row.get("status", "")
        return dto
