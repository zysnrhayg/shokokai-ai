from utils.base_entity import BaseEntity

class FormexportapiDto(BaseEntity):
    # 傾聴内容変換AI帳票出力用DTO
    # フィールド名はプロジェクト規約に従いcamelCaseとする（formcode/reportid/prefecturecode/shokokaicd/source）
    def __init__(self, mode, actflg, triggerid, row, formcode="", reportid="", prefecturecode="", shokokaicd="", source=""):
        super().__init__(mode, actflg, triggerid, row)
        self.formcode = formcode
        self.reportid = reportid
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd
        self.source = source

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return FormexportapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("formcode", ""),
            # report_id（スネークケース）での送信も許容する
            d.get("reportid", d.get("report_id", "")),
            d.get("prefecturecode", ""),
            d.get("shokokaicd", ""),
            d.get("source", ""))
