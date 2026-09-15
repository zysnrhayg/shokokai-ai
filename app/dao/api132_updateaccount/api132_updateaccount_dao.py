#Dao.vm common function
from app.mapper.api132_updateaccount.api132_updateaccount_mapper import api132_updateaccountMapper
import utils.mysqldb_utils

class Api132UpdateaccountDao :

# 関数定義_SQL文_アカウント更新

    def api132_updateaccount(self,dtoObj) :
        prefecture_code = getattr(dtoObj, "prefecturecode", None) or getattr(dtoObj, "prefecture_code", "")
        shokokai_cd = getattr(dtoObj, "shokokaicd", None) or getattr(dtoObj, "shokokai_cd", "")
        user_id = getattr(dtoObj, "userid", None) or getattr(dtoObj, "user_id", "")
        shokuin_kj = getattr(dtoObj, "shokuinkj", None) or getattr(dtoObj, "shokuin_kj", "")
        email = getattr(dtoObj, "email", "")
        status = getattr(dtoObj, "status", "")
        permission_level = getattr(dtoObj, "permissionlevel", None) or getattr(dtoObj, "permission_level", "")
        password = getattr(dtoObj, "password", "") or ""
        user_account_id = getattr(dtoObj, "useraccountid", None) or getattr(dtoObj, "user_account_id", "")
        returnVal = utils.mysqldb_utils.querySQL(
            api132_updateaccountMapper.api132_updateaccount(
                prefecture_code, shokokai_cd, user_id, shokuin_kj, email, status, permission_level, password, user_account_id
            ),
            {
                "prefecture_code": prefecture_code,
                "shokokai_cd": shokokai_cd,
                "user_id": user_id,
                "shokuin_kj": shokuin_kj,
                "email": email,
                "status": str(status if status not in (None, "") else 1),
                "permission_level": permission_level,
                "password": password,
                "user_account_id": str(user_account_id),
            },
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
