from utils.base_entity import BaseEntity

class VoiceuploadapiDto(BaseEntity):
    # 傾聴内容変換AI音声ファイル アップロード用DTO
    # audiofile：アップロードされた音声ファイル情報（multipart）、reportid：対象報告書ID（任意）
    def __init__(self, mode, actflg, triggerid, row, audiofile=None, reportid=""):
        super().__init__(mode, actflg, triggerid, row)
        self.audiofile = audiofile
        self.reportid = reportid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VoiceuploadapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("audiofile", None),
            d.get("reportid", d.get("report_id", "")))
