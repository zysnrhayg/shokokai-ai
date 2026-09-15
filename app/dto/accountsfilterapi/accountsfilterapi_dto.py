from utils.base_entity import BaseEntity

class AccountsfilterapiDto(BaseEntity):
    def __init__(
        self,
        mode,
        actflg,
        triggerid,
        row,
        prefecturecode,
        shokokaicd,
        permissionlevel,
        status,
        corelinked,
        keyword,
        rolecode="",
    ):
        super().__init__(mode, actflg, triggerid, row)
        self.prefecturecode = prefecturecode
        self.shokokaicd = shokokaicd
        self.permissionlevel = permissionlevel
        self.status = status
        self.corelinked = corelinked
        self.keyword = keyword
        self.rolecode = rolecode

    @staticmethod
    def dict_to_json(d):
        if d is None:
            d = {}
        return AccountsfilterapiDto(
            d.get("mode", ""),
            d.get("actflg", ""),
            d.get("triggerid", ""),
            d.get("row", ""),
            d.get("prefecturecode", d.get("prefecture_code", "")),
            d.get("shokokaicd", d.get("shokokai_cd", "")),
            d.get("permissionlevel", d.get("permission_level", "")),
            d.get("status", ""),
            d.get("corelinked", d.get("core_linked", "")),
            d.get("keyword", ""),
            d.get("rolecode", d.get("role_code", "")),
        )
