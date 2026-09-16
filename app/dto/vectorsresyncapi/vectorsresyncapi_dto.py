from utils.base_entity import BaseEntity


class VectorsresyncapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, vectorcollectionid="", vectorcount=""):
        super().__init__(mode, actflg, triggerid, row)
        self.vectorcollectionid = vectorcollectionid
        self.vectorcount = vectorcount

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        dto = VectorsresyncapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", {}),
            "", "")
        # DTOパラメータはrow配下から取得する（フロントエンド呼び出し規約に合わせる）
        row = d.get("row", {}) if isinstance(d.get("row", {}), dict) else {}
        dto.vectorcollectionid = row.get("vectorcollectionid", "") or row.get("vector_collection_id", "")
        dto.vectorcount = row.get("vectorcount", "") or row.get("vector_count", "")
        return dto
