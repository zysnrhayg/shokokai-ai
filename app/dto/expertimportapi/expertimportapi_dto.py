from utils.base_entity import BaseEntity

class ExpertimportapiDto(BaseEntity):
    # 専門家報告取込用DTO
    def __init__(self, mode, actflg, triggerid, row, filename="", formcode=""):
        super().__init__(mode, actflg, triggerid, row)
        self.filename = filename
        self.formcode = formcode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return ExpertimportapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("filename", ""),
            d.get("formcode", ""))
