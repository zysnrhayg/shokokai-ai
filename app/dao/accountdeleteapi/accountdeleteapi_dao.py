from app.mapper.accountdeleteapi.accountdeleteapi_mapper import accountdeleteapiMapper
import utils.mysqldb_utils

class AccountdeleteapiDao:
    def accountdeleteapi(self, dtoObj, deleted_by=""):
        user_account_id = getattr(dtoObj, "useraccountid", None) or getattr(dtoObj, "user_account_id", "")
        returnVal = utils.mysqldb_utils.querySQL(
            accountdeleteapiMapper.accountdeleteapi(user_account_id, deleted_by),
            {
                "user_account_id": str(user_account_id),
                "deleted_by": str(deleted_by or ""),
            },
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
