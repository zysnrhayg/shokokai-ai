from utils.base_entity import BaseEntity

class EntryforminitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, id=""):
        super().__init__(mode, actflg, triggerid, row)
        # 編集対象の知識データID
        self.id = id

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = EntryforminitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}),
            "")
        # DTOパラメータはrow配下から取得する（フロントエンド呼び出し規約に合わせる）
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        dto.id = row.get("id", "") or row.get("knowledgeentryid", "") or row.get("knowledge_entry_id", "")
        return dto
