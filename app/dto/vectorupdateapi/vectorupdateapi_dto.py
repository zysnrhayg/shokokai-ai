from utils.base_entity import BaseEntity


class VectorupdateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, vectorcollectionid="", name="", vectorcount="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.vectorcollectionid = vectorcollectionid
        self.name = name
        self.vectorcount = vectorcount
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = VectorupdateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}),
            "", "", "", "")
        # DTOパラメータはrow配下から取得する（フロントエンド呼び出し規約に合わせる）
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        dto.vectorcollectionid = row.get("vectorcollectionid", "") or row.get("vector_collection_id", "")
        dto.name = row.get("name", "")
        dto.vectorcount = row.get("vector_count", "") or row.get("vectorcount", "")
        dto.status = row.get("status", "")
        return dto
