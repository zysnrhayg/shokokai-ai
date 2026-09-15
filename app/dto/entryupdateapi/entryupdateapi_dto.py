from utils.base_entity import BaseEntity

class EntryupdateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, knowledgeentryid="", title="", knowledgedocumentid="", prefecturecode="", content="", themeids="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        # 更新対象の知識データID
        self.knowledgeentryid = knowledgeentryid
        self.title = title
        # 紐付ファイル（原本文書ID）
        self.knowledgedocumentid = knowledgedocumentid
        # 適用範囲（県コード）
        self.prefecturecode = prefecturecode
        # 本文（trn_knowledge_entry.contentに対応する）
        self.content = content
        # テーマID（カンマ区切り）
        self.themeids = themeids
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = EntryupdateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}),
            "", "", "", "", "", "", "")
        # DTOパラメータはrow配下から取得する（フロントエンド呼び出し規約に合わせる）
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        dto.knowledgeentryid = row.get("knowledgeentryid", "") or row.get("knowledge_entry_id", "")
        dto.title = row.get("title", "")
        dto.knowledgedocumentid = row.get("knowledgedocumentid", "")
        dto.prefecturecode = row.get("prefecturecode", "")
        dto.content = row.get("content", "")
        dto.themeids = row.get("themeids", "")
        dto.status = row.get("status", "")
        return dto
