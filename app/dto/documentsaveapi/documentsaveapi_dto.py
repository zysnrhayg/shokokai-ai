from utils.base_entity import BaseEntity

class DocumentsaveapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, title="", category="", format="", prefecturecode="", filepath="", filesizekb="", status=""):
        super().__init__(mode, actflg, triggerid, row)
        self.title = title
        self.category = category
        self.format = format
        self.prefecturecode = prefecturecode
        self.filepath = filepath
        self.filesizekb = filesizekb
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        row = d.get("row", {})
        if not isinstance(row, dict):
            row = {}
        return DocumentsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            row.get("title", ""),
            row.get("category", ""),
            row.get("format", "PDF"),
            row.get("prefecturecode", "") or row.get("prefecture_code", ""),
            row.get("filepath", "") or row.get("file_path", ""),
            row.get("filesizekb", "0") or row.get("file_size_kb", "0"),
            row.get("status", "審査中")
        )
