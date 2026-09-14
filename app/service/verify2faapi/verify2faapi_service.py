#BasicService.vm
#make Service templete
import json
import utils.config
import threading
import utils.json_constant	
from flask import session 
from app.common.getautonum import GetAutonum
from datetime import datetime, timezone, timedelta
import utils.date_util
from utils.jsonwfc_object import JSONWFCObject
import resources.messages
from app.dao.api105_authenticateuser.api105_authenticateuser_dao import Api105AuthenticateuserDao
from app.dao.api106_gettrusteddevice.api106_gettrusteddevice_dao import Api106GettrusteddeviceDao
from app.dao.api107_inserttrusteddevice.api107_inserttrusteddevice_dao import Api107InserttrusteddeviceDao
from app.dto.api105_authenticateuser.api105_authenticateuser_dto import Api105AuthenticateuserDto
from app.dto.api106_gettrusteddevice.api106_gettrusteddevice_dto import Api106GettrusteddeviceDto
from app.dto.api107_inserttrusteddevice.api107_inserttrusteddevice_dto import Api107InserttrusteddeviceDto
from app.dto.verify2faapi.verify2faapi_dto import Verify2faapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class Verify2faapiService :

	#	# 
	# 二要素認証画面認証ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def verify2faapi(self,verify2faapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		CODE = verify2faapi_dto.code#GeninusClientScript 1318
		REMEMBER_DEVICE = verify2faapi_dto.rememberdevice#GeninusClientScript 1318
		api105_authenticateuser = Api105AuthenticateuserDto.dict_to_json({}) #CommonFunction 110
		api105_authenticateuserList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api105_authenticateuser_dto = None #ResultGenerator 119
		#ResultGenerator365
		USERACCOUNTID = ""
		PREFECTURECODE = ""
		SHOKOKAICD = ""
		USERID = ""
		SHOKUINKJ = ""
		PASSWORD = ""
		STATUS = ""
		TOTPSECRET = ""
		ISMFAENABLED = ""
		FAILEDLOGINCOUNT = ""
		LOCKEDUNTIL = ""
		api106_gettrusteddevice = Api106GettrusteddeviceDto.dict_to_json({}) #CommonFunction 110
		api106_gettrusteddeviceList = None #ResultGenerator 72
		#_dto api106_gettrusteddevice_dto = None #ResultGenerator 119
		TRUSTEDDEVICEID = ""
		EXPIRESAT = ""
		api107_inserttrusteddevice = Api107InserttrusteddeviceDto.dict_to_json({}) #CommonFunction 110
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#二要素認証画面認証ボタン_Verify2faAPI_(API)
			
			#「項目処理」（共通関数:Verify2faAPI）,パラメータは（code,remember_device）
			
			#以下の処理を行う。
			
			#関数「API105_AuthenticateUser」の「db_API105_AuthenticateUser」メソッドを行う,パラメータは「prefecture_code,user_id」,戻り値設定は「<user_account_id>=user_account_id,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<user_id>=user_id,<shokuin_kj>=shokuin_kj,<password>=password,<status>=status,<totp_secret>=totp_secret,<is_mfa_enabled>=is_mfa_enabled,<failed_login_count>=failed_login_count,<locked_until>=locked_until」を設定する。
			
			# prefecture_code
			api105_authenticateuser.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# user_id
			api105_authenticateuser.userid = USER_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api105_authenticateuserList = Api105AuthenticateuserDao().api105_authenticateuser(api105_authenticateuser)
			api105_authenticateuserlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api105_authenticateuserList != None :
				api105_authenticateuserlistVar = api105_authenticateuserList.fetchall() if hasattr(api105_authenticateuserList, 'fetchall') else api105_authenticateuserList
			if api105_authenticateuserlistVar != None and len(api105_authenticateuserlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api105_authenticateuserlistVar))
			# --LINE114 retrieved first value
			if api105_authenticateuserlistVar != None and len(api105_authenticateuserlistVar) > 0 :
				rec = api105_authenticateuserlistVar[0]
				USERACCOUNTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_account_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAICD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")) # ResultGenerator 385
				# ResultGenerator 385
				
				USERID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKUINKJ = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokuin_kj")) # ResultGenerator 385
				# ResultGenerator 385
				
				PASSWORD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "password")) # ResultGenerator 385
				# ResultGenerator 385
				
				STATUS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status")) # ResultGenerator 385
				# ResultGenerator 385
				
				TOTPSECRET = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "totp_secret")) # ResultGenerator 385
				# ResultGenerator 385
				
				ISMFAENABLED = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "is_mfa_enabled")) # ResultGenerator 385
				# ResultGenerator 385
				
				FAILEDLOGINCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "failed_login_count")) # ResultGenerator 385
				# ResultGenerator 385
				
				LOCKEDUNTIL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "locked_until")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API106_GetTrustedDevice」の「db_API106_GetTrustedDevice」メソッドを行う,パラメータは「user_account_id,token_hash」,戻り値設定は「<trusted_device_id>=trusted_device_id,<user_account_id>=user_account_id,<expires_at>=expires_at」を設定する。
			
			# user_account_id
			api106_gettrusteddevice.useraccountid = USERACCOUNTID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# token_hash
			api106_gettrusteddevice.tokenhash = TOKEN_HASH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api106_gettrusteddeviceList = Api106GettrusteddeviceDao().api106_gettrusteddevice(api106_gettrusteddevice)
			api106_gettrusteddevicelistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api106_gettrusteddeviceList != None :
				api106_gettrusteddevicelistVar = api106_gettrusteddeviceList.fetchall() if hasattr(api106_gettrusteddeviceList, 'fetchall') else api106_gettrusteddeviceList
			if api106_gettrusteddevicelistVar != None and len(api106_gettrusteddevicelistVar) > 0 :
				SHUTOKUKENSUU = str(len(api106_gettrusteddevicelistVar))
			# --LINE114 retrieved first value
			if api106_gettrusteddevicelistVar != None and len(api106_gettrusteddevicelistVar) > 0 :
				rec = api106_gettrusteddevicelistVar[0]
				TRUSTEDDEVICEID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "trusted_device_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				USERACCOUNTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_account_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				EXPIRESAT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "expires_at")) # ResultGenerator 385
				# ResultGenerator 385
				
			#<remember_device>が"true"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if REMEMBER_DEVICE.replace(" ", "") == "true" : #GeniusContion 823
				#GeniusContion 823
				#関数「API107_InsertTrustedDevice」の「db_API107_InsertTrustedDevice」メソッドを行う,パラメータは「user_account_id,token_hash,expires_at」。
				
				# user_account_id
				api107_inserttrusteddevice.useraccountid = USERACCOUNTID #ArgumentGenerator 274
				#ArgumentGenerator 274
				
				# token_hash
				api107_inserttrusteddevice.tokenhash = TOKEN_HASH #ArgumentGenerator 274
				#ArgumentGenerator 274
				
				# expires_at
				api107_inserttrusteddevice.expiresat = EXPIRESAT #ArgumentGenerator 274
				#ArgumentGenerator 274
				
				Api107InserttrusteddeviceDao().api107_inserttrusteddevice(api107_inserttrusteddevice) #ResultGenerator 104
				#ResultGenerator 104
				#処理終了。
				pass
				#GeniusClientScript 1207
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
