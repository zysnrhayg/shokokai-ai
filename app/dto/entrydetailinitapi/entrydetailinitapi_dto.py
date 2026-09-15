from utils.base_entity import BaseEntity

class EntrydetailinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, knowledgeentryid=""):
        super().__init__(mode, actflg, triggerid, row)
        # 詳細表示対象の知識データID
        self.knowledgeentryid = knowledgeentryid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = EntrydetailinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}),
            "")
        # DTOパラメータはrow配下から取得する（フロントエンド呼び出し規約に合わせる）
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        dto.knowledgeentryid = row.get("knowledgeentryid", "") or row.get("knowledge_entry_id", "")
        return dto
