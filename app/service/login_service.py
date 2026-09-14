from app.dao.login_dao import LoginDao 
from flask import request, session 
import utils.config 
from utils.jsonwfc_object import JSONWFCObject 
import utils.string_util 
from utils.menurightutil import MenuRightUtil 
from utils.encrypt import hash_password, is_bcrypt_hash, verify_password 
import utils.session_constant  
from logger import currentLog  

def _user_eff_from_row(row) -> str:
	if row is None:
		return ""
	if isinstance(row, dict):
		value = row.get("user_eff")
		if value is None:
			value = row.get("enabled_flag")
		return str(value if value is not None else "").strip()
	return str(getattr(row, "user_eff", None) or getattr(row, "enabled_flag", None) or "").strip()

def _is_user_login_enabled(row) -> bool:
	"""ユーザーが有効状態の「1」であるかを判定する。"""
	return _user_eff_from_row(row) == "1"

def _upgrade_legacy_password(loginid: str, plain: str, stored: str, admin: bool = False) -> None:
	"""旧 SHA-1 認証の成功直後に保存値を bcrypt へ更新する。"""
	if is_bcrypt_hash(str(stored or "").strip()):
		return
	new_hash = hash_password(plain)
	updated = (LoginDao.updateAdminPasswordAfterLogin(loginid, new_hash)
		if admin else LoginDao.updateUserPasswordAfterLogin(loginid, new_hash))
	if updated != 1:
		raise RuntimeError("旧形式パスワードの更新件数が1件ではありません。")
	currentLog.getLog(loginid).info(
		"旧形式パスワードをbcryptへ更新しました: login_id=%s, account_type=%s",
		loginid, "管理者" if admin else "一般ユーザー")

#**
# * EDI請求管理システム# Page: login
# */
class LoginService :

	loginid = ""
	groupID = ""
	userSurname = ""
	userName = ""
	def dologin(self,loginid,password) :
		jsonObj = JSONWFCObject()
		alUserInfo = []
		menuRightUtil = MenuRightUtil()

		# login_tableid取得
		login_tableid = utils.config.user_tableid
		# login_id取得
		login_id = utils.config.user_table_userid_fieldid
		# login_password取得
		login_password = utils.config.user_table_password_fieldid
		# userId取得
		userId = utils.config.user_table_user_fieldid
		# user_eff取得
		user_eff = utils.config.user_table_eff_status_fieldid
		# user_Group取得
		user_Group = utils.config.user_table_group_fieldid
		# usernm1取得
		usernm1 = utils.config.user_table_usernm1_fieldid
		# usernm2取得
		usernm2 = utils.config.user_table_usernm2_fieldid

		if loginid != "admin" and utils.string_util.isNullOrBlank(login_tableid) == False and utils.string_util.isNullOrBlank(login_id) == False and utils.string_util.isNullOrBlank(login_password) == False and utils.string_util.isNullOrBlank(user_Group) == False :

			alUserInfo = LoginDao.loginGetByLoginId(login_id , login_password, user_Group , login_tableid, loginid)
			#ログインユーザー情報を空白すると情報 : 
			a = None
			if alUserInfo != None and len(alUserInfo) > 0 :
				row = alUserInfo[0]
				db_hashed = row.get("password") if isinstance(row, dict) else getattr(row, "password", None)
				if verify_password(password, db_hashed) :
					_upgrade_legacy_password(loginid, password, db_hashed)
					a = row
			if a == None :

				alUserInfo = LoginDao.getAdminByUsername(loginid)
				#ログインユーザー情報を空白すると情報 : 会員Noかパスワードが間違っています。
				a = None
				if alUserInfo and len(alUserInfo) > 0 :
					admin_row = alUserInfo[0]
					admin_hashed = ((admin_row.get("PASSWORD") or admin_row.get("password")) if isinstance(admin_row, dict) else (getattr(admin_row, "PASSWORD", None) or getattr(admin_row, "password", None)))
					if verify_password(password, admin_hashed) :
						_upgrade_legacy_password(loginid, password, admin_hashed, admin=True)
						a = admin_row
				if a == None :
					jsonObj.setValue("i", "会員Noかパスワードが間違っています。")
					return jsonObj.toJsonString()
				else :
					self.loginid = loginid
					self.userSurname = loginid
					self.userName = loginid
					self.setLoginSession()
					menuRightUtil.setAdminSessionRight(session)
					return "OK"
			else : 

				if not _is_user_login_enabled(a):
					jsonObj.setValue("i", "ユーザーはロックされました。システム管理者に連絡してください。");
					return jsonObj.toJsonString()
				else : 
					# loginid取得
					self.loginid = a.get("loginid") if isinstance(a, dict) else getattr(a, "loginid", None)
					# groupID取得
					self.groupID = a.get("groupid") if isinstance(a, dict) else getattr(a, "groupid", None)
					# usernm1取得
					#self.userSurname = a.usernm1
					# usernm2取得
					#self.userName = a.usernm2
					#menuRightUtil.setSessionRight(session, self.groupID)
					# Sessionを設定
					self.setLoginSession()
					jsonObj.setScript("username", usernm1)
				
					jsonObj.setScript("OK", "./null")
					return jsonObj.toJsonString()
		else : 

			alUserInfo = LoginDao.getAdminByUsername(loginid)
			#ログインユーザー情報を空白すると情報 : 会員Noかパスワードが間違っています。
			if  alUserInfo == None or len(alUserInfo) == 0 :
				jsonObj.setValue("i", "会員Noかパスワードが間違っています。");
				return jsonObj.toJsonString()
			else :
				admin_row = alUserInfo[0]
				admin_hashed = ((admin_row.get("PASSWORD") or admin_row.get("password")) if isinstance(admin_row, dict) else (getattr(admin_row, "PASSWORD", None) or getattr(admin_row, "password", None)))
				if not verify_password(password, admin_hashed) :
					jsonObj.setValue("i", "会員Noかパスワードが間違っています。");
					return jsonObj.toJsonString()
				_upgrade_legacy_password(loginid, password, admin_hashed, admin=True)
				self.userSurname = loginid
				self.userName = loginid
				self.loginid = loginid
				# Sessionを設定
				self.setLoginSession()
				menuRightUtil.setAdminSessionRight(session)
				jsonObj.setScript("OK", "./null")
				jsonObj.setScript("username", "admin")
				return jsonObj.toJsonString()

	# 
	# ログインセッションを設定する
	#
	def setLoginSession(self) :

		# languageID設定
		session[utils.session_constant.LANGUAGE_ID] = "JPN"
		# loginid設定
		session[utils.session_constant.USER_ID] = self.loginid
		session["LOGIN_USER_ID"] = self.loginid
		session[utils.session_constant.APP_USER_ID] = self.loginid
		session["ORGID"] = self.groupID
		# userflg設定
		session[utils.session_constant.USER_FLG] = "OK"
		session["USER_NAME1"] = self.userSurname
		session["USER_NAME2"] = self.userName
		utils.config.global_log = currentLog.getLog(self.loginid)

