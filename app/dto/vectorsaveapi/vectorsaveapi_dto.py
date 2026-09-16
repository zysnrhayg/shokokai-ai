from utils.base_entity import BaseEntity


class VectorsaveapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, name="", collectioncode="", vectorcount="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.name = name
        self.collectioncode = collectioncode
        # ベクトル数とステータス（フロントエンドから送信される）
        self.vectorcount = vectorcount
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = VectorsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}),
            "", "", "", "")
        # DTOパラメータはrow配下から取得する（フロントエンド呼び出し規約に合わせる）
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        dto.name = row.get("name", "")
        dto.collectioncode = row.get("collectioncode", "") or row.get("collection_code", "")
        dto.vectorcount = row.get("vector_count", "") or row.get("vectorcount", "")
        dto.status = row.get("status", "")
        return dto
