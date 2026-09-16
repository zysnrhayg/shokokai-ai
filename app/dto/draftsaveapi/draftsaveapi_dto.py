from utils.base_entity import BaseEntity

class DraftsaveapiDto(BaseEntity):
    # 傾聴内容変換AI下書き保存用DTO
    # houkokushokoumokuisshiki（報告書項目一式）はフロントエンドから送られる報告書項目の辞書
    def __init__(self, mode, actflg, triggerid, row, houkokushokoumokuisshiki=None):
        super().__init__(mode, actflg, triggerid, row)
        self.houkokushokoumokuisshiki = houkokushokoumokuisshiki if houkokushokoumokuisshiki is not None else {}

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return DraftsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("houkokushokoumokuisshiki", d.get("row", {})) if isinstance(d.get("houkokushokoumokuisshiki", d.get("row", {})), dict) else {})
