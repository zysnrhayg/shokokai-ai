#Dao.vm common function
from app.mapper.api131_insertaccount.api131_insertaccount_mapper import api131_insertaccountMapper
import utils.mysqldb_utils

class Api131InsertaccountDao :

# 関数定義_SQL文_アカウント登録

    def api131_insertaccount(self,dtoObj) :
        prefecture_code = getattr(dtoObj, "prefecturecode", None) or getattr(dtoObj, "prefecture_code", "")
        shokokai_cd = getattr(dtoObj, "shokokaicd", None) or getattr(dtoObj, "shokokai_cd", "")
        user_id = getattr(dtoObj, "userid", None) or getattr(dtoObj, "user_id", "")
        shokuin_kj = getattr(dtoObj, "shokuinkj", None) or getattr(dtoObj, "shokuin_kj", "")
        email = getattr(dtoObj, "email", "")
        status = getattr(dtoObj, "status", "")
        core_linked = getattr(dtoObj, "corelinked", None)
        if core_linked is None:
            core_linked = getattr(dtoObj, "core_linked", False)
        permission_level = getattr(dtoObj, "permissionlevel", None) or getattr(dtoObj, "permission_level", "")
        password = getattr(dtoObj, "password", "")
        # PostgreSQL boolean bind: pass true/false strings
        if isinstance(core_linked, bool):
            core_linked_bind = "true" if core_linked else "false"
        else:
            core_linked_bind = "true" if str(core_linked).lower() in ("1", "true", "t", "yes") else "false"
        returnVal = utils.mysqldb_utils.querySQL(
            api131_insertaccountMapper.api131_insertaccount(
                prefecture_code, shokokai_cd, user_id, shokuin_kj, email, status, core_linked_bind, permission_level, password
            ),
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "user_id": user_id,
                "shokuin_kj": shokuin_kj,
                "email": email,
                "status": str(status if status not in (None, "") else 1),
                "core_linked": core_linked_bind,
                "permission_level": permission_level,
                "password": password,
            },
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
