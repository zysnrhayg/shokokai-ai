# LoginDao の参照処理は、検索結果を辞書のリストへ統一して返す。
from app.mapper.login_mapper import LoginMapper
import utils.mysqldb_utils
class LoginDao :
	
	
	def loginInit (LOGINID, LOGINPASSWORD, GROUPID, LOGINTABLEID, WHRLOGINID,WHRLOGINPASSWORD) :

		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.loginInit(LOGINID, LOGINPASSWORD, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD),{"LOGINTABLEID": LOGINTABLEID,"WHRLOGINID": WHRLOGINID,"WHRLOGINPASSWORD": WHRLOGINPASSWORD}))
	def loginGetByLoginId(LOGINID, LOGINPASSWORD, GROUPID, LOGINTABLEID, WHRLOGINID) :
		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.loginGetByLoginId(LOGINID, LOGINPASSWORD, GROUPID, LOGINTABLEID, WHRLOGINID),{"LOGINTABLEID": LOGINTABLEID,"WHRLOGINID": WHRLOGINID}))
	def loginInitNm (LOGINID, LOGINPASSWORD, USER_EFF, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD, USERID, USERNM1, USERNM2) :

		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.loginInitNm(LOGINID, LOGINPASSWORD, USER_EFF, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD, USERID, USERNM1, USERNM2),{"LOGINTABLEID": LOGINTABLEID,"WHRLOGINID": WHRLOGINID,"WHRLOGINPASSWORD": WHRLOGINPASSWORD}))
	def loginInitSurname (LOGINID, LOGINPASSWORD, USER_EFF, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD, USERID, USERNM1) :

		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.loginInitSurname(LOGINID, LOGINPASSWORD, USER_EFF, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD, USERID, USERNM1),{"LOGINTABLEID": LOGINTABLEID,"WHRLOGINID": WHRLOGINID,"WHRLOGINPASSWORD": WHRLOGINPASSWORD}))
	def loginInitName (LOGINID, LOGINPASSWORD, USER_EFF, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD, USERID, USERNM2) :

		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.loginInitName(LOGINID, LOGINPASSWORD, USER_EFF, GROUPID, LOGINTABLEID, WHRLOGINID, WHRLOGINPASSWORD, USERID, USERNM2),{"LOGINTABLEID": LOGINTABLEID,"WHRLOGINID": WHRLOGINID,"WHRLOGINPASSWORD": WHRLOGINPASSWORD}))
	def loginAdminInit (LOGINID, PASSWORD) :

		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.loginAdminInit(LOGINID, PASSWORD),{"LOGINID":LOGINID,"PASSWORD": PASSWORD}))
	def getAdminByUsername(LOGINID) :
		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(LoginMapper.getAdminByUsername(LOGINID),{"LOGINID": LOGINID}))
	def updateUserPasswordAfterLogin(LOGINID, PASSWORD) :
		result = utils.mysqldb_utils.updateSQL(LoginMapper.updateUserPasswordAfterLogin(LOGINID, PASSWORD), {"LOGINID": LOGINID, "PASSWORD": PASSWORD})
		if result is None or not hasattr(result, "rowcount"):
			raise RuntimeError("一般ユーザーパスワードの更新結果を取得できません。")
		return result.rowcount
	def updateAdminPasswordAfterLogin(LOGINID, PASSWORD) :
		result = utils.mysqldb_utils.updateSQL(LoginMapper.updateAdminPasswordAfterLogin(LOGINID, PASSWORD), {"LOGINID": LOGINID, "PASSWORD": PASSWORD})
		if result is None or not hasattr(result, "rowcount"):
			raise RuntimeError("管理者パスワードの更新結果を取得できません。")
		return result.rowcount

