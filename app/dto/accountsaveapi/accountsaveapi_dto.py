from utils.base_entity import BaseEntity

class AccountsaveapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, prefecturecode, shokokaicd, userid, shokuinkj, email, password, permissionlevel, status):
        super().__init__(mode, actflg, triggerid, row)
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd
        self.userid = userid
        self.shokuinkj = shokuinkj
        self.email = email
        self.password = password
        self.permissionlevel = permissionlevel
        self.status = status

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AccountsaveapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("prefecturecode", d.get("prefecture_code", "")),
            d.get("shokokaicd", d.get("shokokai_cd", "")),
            d.get("userid", d.get("user_id", "")),
            d.get("shokuinkj", d.get("shokuin_kj", "")),
            d.get("email", ""),
            d.get("password", ""),
            d.get("permissionlevel", d.get("permission_level", "")),
            d.get("status", ""))
