from app.mapper.api106_gettrusteddevice.api106_gettrusteddevice_mapper import api106_gettrusteddeviceMapper
import utils.mysqldb_utils


class Api106GettrusteddeviceDao:

    def api106_gettrusteddevice(self, dtoObj):
        user_account_id = getattr(dtoObj, "useraccountid", None) or getattr(dtoObj, "user_account_id", "")
        token_hash = getattr(dtoObj, "tokenhash", None) or getattr(dtoObj, "token_hash", "")
        returnVal = utils.mysqldb_utils.querySQL(
            api106_gettrusteddeviceMapper.api106_gettrusteddevice(user_account_id, token_hash),
            {"user_account_id": user_account_id, "token_hash": token_hash},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
