from utils.base_entity import BaseEntity

class AccountsinitapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, prefecturecode, onlyfederation, excludefederation, rolecode, shokokaicd, federationcd, limit="", offset=""):
        super().__init__(mode, actflg, triggerid, row)
        self.prefecturecode = prefecturecode
        self.onlyfederation = onlyfederation
        self.excludefederation = excludefederation
        self.rolecode = rolecode
        self.shokokaicd = shokokaicd
        self.federationcd = federationcd
        self.limit = limit
        self.offset = offset

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AccountsinitapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("prefecturecode", d.get("prefecture_code", "")),
            d.get("onlyfederation", d.get("only_federation", "")),
            d.get("excludefederation", d.get("exclude_federation", "")),
            d.get("rolecode", d.get("role_code", "")),
            d.get("shokokaicd", d.get("shokokai_cd", "")),
            d.get("federationcd", d.get("federation_cd", "")),
            d.get("limit", ""),
            d.get("offset", ""),
        )