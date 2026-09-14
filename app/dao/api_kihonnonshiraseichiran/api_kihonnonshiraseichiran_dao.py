from app.mapper.api_kihonnonshiraseichiran.api_kihonnonshiraseichiran_mapper import api_kihonnonshiraseichiranMapper
import utils.mysqldb_utils


class ApiKihonnonshiraseichiranDao:

    def api_kihonnonshiraseichiran(self, dtoObj):
        role_code = getattr(dtoObj, "rolecode", None) or getattr(dtoObj, "role_code", "")
        returnVal = utils.mysqldb_utils.querySQL(
            api_kihonnonshiraseichiranMapper.api_kihonnonshiraseichiran(role_code),
            {"role_code": role_code},
        )
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
