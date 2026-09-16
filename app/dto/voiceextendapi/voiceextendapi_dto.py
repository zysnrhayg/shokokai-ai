from utils.base_entity import BaseEntity

class VoiceextendapiDto(BaseEntity):
    # 傾聴内容変換AI録音時間 ＋30分延長用DTO
    # addseconds：延長秒数、timeremaining/timetotal：現在の残り時間・合計時間（秒）
    def __init__(self, mode, actflg, triggerid, row, reportid="", addseconds="1800", timeremaining="", timetotal=""):
        super().__init__(mode, actflg, triggerid, row)
        self.reportid = reportid
        self.addseconds = addseconds
        self.timeremaining = timeremaining
        self.timetotal = timetotal

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return VoiceextendapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("reportid", d.get("report_id", "")),
            d.get("addseconds", d.get("add_seconds", "1800")),
            d.get("timeremaining", d.get("timer_remaining", "")),
            d.get("timetotal", d.get("timer_total", "")))
