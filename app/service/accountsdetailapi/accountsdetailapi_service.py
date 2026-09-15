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
from app.dao.api103_getaccountdetail.api103_getaccountdetail_dao import Api103GetaccountdetailDao
from app.dto.accountsdetailapi.accountsdetailapi_dto import AccountsdetailapiDto
from app.dto.api103_getaccountdetail.api103_getaccountdetail_dto import Api103GetaccountdetailDto
from app.common.account_json import put_account_on_json
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AccountsdetailapiService :

	#	# 
	# アカウント一覧画面詳細ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accountsdetailapi(self,accountsdetailapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		USER_ACCOUNT_ID = accountsdetailapi_dto.useraccountid#GeninusClientScript 1318
		api103_getaccountdetail = Api103GetaccountdetailDto.dict_to_json({}) #CommonFunction 110
		api103_getaccountdetailList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api103_getaccountdetail_dto = None #ResultGenerator 119
		#ResultGenerator365
		USERACCOUNTID = ""
		PREFECTURECODE = ""
		SHOKOKAICD = ""
		USERID = ""
		SHOKUINKJ = ""
		EMAIL = ""
		STATUS = ""
		CORELINKED = ""
		PERMISSIONLEVEL = ""
		LASTLOGINAT = ""
		PREFECTURENAME = ""
		SHOKOKAINAME = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント一覧画面詳細ボタン_AccountsDetailAPI_(API)
			
			#「項目処理」（共通関数:AccountsDetailAPI）,パラメータは（user_account_id）
			
			#以下の処理を行う。
			
			#関数「API103_GetAccountDetail」の「db_API103_GetAccountDetail」メソッドを行う,パラメータは「user_account_id」,戻り値設定は「<user_account_id>=user_account_id,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<user_id>=user_id,<shokuin_kj>=shokuin_kj,<email>=email,<status>=status,<core_linked>=core_linked,<permission_level>=permission_level,<last_login_at>=last_login_at,<prefecture_name>=prefecture_name,<shokokai_name>=shokokai_name」を設定する。
			
			# user_account_id
			api103_getaccountdetail.useraccountid = USER_ACCOUNT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api103_getaccountdetailList = Api103GetaccountdetailDao().api103_getaccountdetail(api103_getaccountdetail)
			api103_getaccountdetaillistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api103_getaccountdetailList != None :
				api103_getaccountdetaillistVar = api103_getaccountdetailList.fetchall() if hasattr(api103_getaccountdetailList, 'fetchall') else api103_getaccountdetailList
			if api103_getaccountdetaillistVar != None and len(api103_getaccountdetaillistVar) > 0 :
				SHUTOKUKENSUU = str(len(api103_getaccountdetaillistVar))
			# --LINE114 retrieved first value
			if api103_getaccountdetaillistVar != None and len(api103_getaccountdetaillistVar) > 0 :
				rec = api103_getaccountdetaillistVar[0]
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
				
				EMAIL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "email")) # ResultGenerator 385
				# ResultGenerator 385
				
				STATUS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status")) # ResultGenerator 385
				# ResultGenerator 385
				
				CORELINKED = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "core_linked")) # ResultGenerator 385
				# ResultGenerator 385
				
				PERMISSIONLEVEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "permission_level")) # ResultGenerator 385
				# ResultGenerator 385
				
				LASTLOGINAT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "last_login_at")) # ResultGenerator 385
				# ResultGenerator 385
				
				PREFECTURENAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAINAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_name")) # ResultGenerator 385
				# ResultGenerator 385
				put_account_on_json(jsonObj, rec)
			else:
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "アカウントが見つかりません")
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
