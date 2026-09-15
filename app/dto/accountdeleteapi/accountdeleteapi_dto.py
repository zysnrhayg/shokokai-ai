from utils.base_entity import BaseEntity

class AccountdeleteapiDto(BaseEntity):
    def __init__(self, mode, actflg, triggerid, row, useraccountid):
        super().__init__(mode, actflg, triggerid, row)
        self.useraccountid = useraccountid

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AccountdeleteapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("useraccountid", d.get("user_account_id", "")))
