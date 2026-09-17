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
from app.accounts.write_helpers import find_live_account_id, replace_account_qualifications
from app.dao.api131_insertaccount.api131_insertaccount_dao import Api131InsertaccountDao
from app.dto.accountsaveapi.accountsaveapi_dto import AccountsaveapiDto
from app.dto.api131_insertaccount.api131_insertaccount_dto import Api131InsertaccountDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util
from utils.encrypt import encrypt_for_storage




class AccountsaveapiService :

	#	# 
	# アカウント新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accountsaveapi(self,accountsaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		PREFECTURE_CODE = accountsaveapi_dto.prefecturecode#GeninusClientScript 1318
		SHOKOKAI_CD = accountsaveapi_dto.shokokaicd#GeninusClientScript 1318
		USER_ID = accountsaveapi_dto.userid#GeninusClientScript 1318
		SHOKUIN_KJ = accountsaveapi_dto.shokuinkj#GeninusClientScript 1318
		EMAIL = accountsaveapi_dto.email#GeninusClientScript 1318
		PASSWORD = accountsaveapi_dto.password#GeninusClientScript 1318
		PERMISSION_LEVEL = accountsaveapi_dto.permissionlevel#GeninusClientScript 1318
		STATUS = accountsaveapi_dto.status#GeninusClientScript 1318
		QUALIFICATION_CODES = getattr(accountsaveapi_dto, "qualificationcodes", "")
		CORE_LINKED = False
		api131_insertaccount = Api131InsertaccountDto.dict_to_json({}) #CommonFunction 110
		#_dto api131_insertaccount_dto = None #ResultGenerator 119
		#ResultGenerator365
		USERACCOUNTID = ""
		TOUROKUKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント新規画面登録ボタン_AccountSaveAPI_(API)
			
			#「項目処理」（共通関数:AccountSaveAPI）,パラメータは（prefecture_code,shokokai_cd,user_id,shokuin_kj,email,password,permission_level,status）
			
			#以下の処理を行う。
			
			#関数「API131_InsertAccount」の「db_API131_InsertAccount」メソッドを行う,パラメータは「prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,core_linked,permission_level,password」,戻り値設定は「<user_account_id>=user_account_id」を設定する。

			if find_live_account_id(PREFECTURE_CODE, USER_ID):
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "このユーザIDは既に使用されています")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				return
			
			# prefecture_code
			api131_insertaccount.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api131_insertaccount.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# user_id
			api131_insertaccount.userid = USER_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokuin_kj
			api131_insertaccount.shokuinkj = SHOKUIN_KJ #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# email
			api131_insertaccount.email = EMAIL #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# status
			api131_insertaccount.status = STATUS if STATUS not in (None, "") else 1 #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# core_linked
			api131_insertaccount.corelinked = CORE_LINKED #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# permission_level
			api131_insertaccount.permissionlevel = PERMISSION_LEVEL #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# password
			api131_insertaccount.password = encrypt_for_storage(PASSWORD) if PASSWORD not in (None, "") else "" #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			api131_insertaccountlistVar = Api131InsertaccountDao().api131_insertaccount(api131_insertaccount) #ResultGenerator 104
			#ResultGenerator 104
			# --LINE114 retrieved first value
			if api131_insertaccountlistVar != None and len(api131_insertaccountlistVar) > 0 :
				rec = api131_insertaccountlistVar[0]
				USERACCOUNTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_account_id")) # ResultGenerator 385
				# ResultGenerator 385
				TOUROKUKENSUU = "1"
			#<登録件数>が"1"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if TOUROKUKENSUU.replace(" ", "") == "1" : #GeniusContion 823
				#GeniusContion 823
				replace_account_qualifications(USERACCOUNTID, QUALIFICATION_CODES)
				#「登録しました」メッセージを表示する。
				jsonObj.setValue("useraccountid", USERACCOUNTID)
				jsonObj.setValue("user_account_id", USERACCOUNTID)
				jsonObj.setValue(utils.json_constant.JSONID_MSG, "登録しました")
				#処理終了。
				pass
				#GeniusClientScript 1207
			else:
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "登録に失敗しました")
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
