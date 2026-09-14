from app.mapper.api105_authenticateuser.api105_authenticateuser_mapper import api105_authenticateuserMapper
import utils.mysqldb_utils


class Api105AuthenticateuserDao:

    def api105_authenticateuser(self, dtoObj):
        prefecture_code = getattr(dtoObj, "prefecturecode", None) or getattr(dtoObj, "prefecture_code", "")
        user_id = getattr(dtoObj, "userid", None) or getattr(dtoObj, "user_id", "")
        returnVal = utils.mysqldb_utils.querySQL(
            api105_authenticateuserMapper.api105_authenticateuser(prefecture_code, user_id),
            {"prefecture_code": prefecture_code, "user_id": user_id},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
