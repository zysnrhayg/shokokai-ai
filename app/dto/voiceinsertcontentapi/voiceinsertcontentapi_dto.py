from utils.base_entity import BaseEntity

class VoiceinsertcontentapiDto(BaseEntity):
    # 傾聴内容変換AI文字起こしを内容欄に反映用DTO
    # transcript：内容欄へ反映する文字起こしテキスト
    def __init__(self, mode, actflg, triggerid, row, transcript=""):
        super().__init__(mode, actflg, triggerid, row)
        self.transcript = transcript

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VoiceinsertcontentapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("transcript", ""))
