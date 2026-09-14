from utils.base_entity import BaseEntity


class LoginapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, prefecturecode="", userid="", password="", remember=""):
        super().__init__(mode, actflg, triggerid, row)
        self.prefecturecode = prefecturecode
        self.userid = userid
        self.password = password
        self.remember = remember

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return LoginapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("prefecturecode") or d.get("prefecture_code", ""),
            d.get("userid") or d.get("user_id", ""),
            d.get("password", ""),
            d.get("remember") or d.get("remember_device", ""),
        )
