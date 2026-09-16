from utils.base_entity import BaseEntity

class AiformatapiDto(BaseEntity):
    # 傾聴内容変換AI文字起こし AI整形用DTO
    # transcript：整形対象の文字起こしテキスト
    def __init__(self, mode, actflg, triggerid, row, transcript=""):
        super().__init__(mode, actflg, triggerid, row)
        self.transcript = transcript

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AiformatapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("transcript", ""))
