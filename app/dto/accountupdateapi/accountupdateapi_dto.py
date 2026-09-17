from utils.base_entity import BaseEntity

class AccountupdateapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, useraccountid, prefecturecode, shokokaicd, userid, shokuinkj, email, password, permissionlevel, status, qualificationcodes=""):
        super().__init__(mode, actflg, triggerid, row)
        self.useraccountid = useraccountid
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd
        self.userid = userid
        self.shokuinkj = shokuinkj
        self.email = email
        self.password = password
        self.permissionlevel = permissionlevel
        self.status = status
        self.qualificationcodes = qualificationcodes

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AccountupdateapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("useraccountid", d.get("user_account_id", "")),
            d.get("prefecturecode", d.get("prefecture_code", "")),
            d.get("shokokaicd", d.get("shokokai_cd", "")),
            d.get("userid", d.get("user_id", "")),
            d.get("shokuinkj", d.get("shokuin_kj", "")),
            d.get("email", ""),
            d.get("password", ""),
            d.get("permissionlevel", d.get("permission_level", "")),
            d.get("status", ""),
            d.get("qualificationcodes", d.get("qualification_codes", "")))
