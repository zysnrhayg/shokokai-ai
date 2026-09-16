from utils.base_entity import BaseEntity

class VoicerecordapiDto(BaseEntity):
    # 傾聴内容変換AI音声録音 開始／停止用DTO
    # action：start｜stop、reportid：対象報告書ID（任意）
    def __init__(self, mode, actflg, triggerid, row, action="", reportid=""):
        super().__init__(mode, actflg, triggerid, row)
        self.action = action
        self.reportid = reportid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VoicerecordapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("action", ""),
            d.get("reportid", d.get("report_id", "")))
