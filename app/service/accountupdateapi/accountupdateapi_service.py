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
from app.dao.api132_updateaccount.api132_updateaccount_dao import Api132UpdateaccountDao
from app.dto.accountupdateapi.accountupdateapi_dto import AccountupdateapiDto
from app.dto.api132_updateaccount.api132_updateaccount_dto import Api132UpdateaccountDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util
from utils.encrypt import encrypt_for_storage




class AccountupdateapiService :

	#	# 
	# アカウント編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accountupdateapi(self,accountupdateapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		USER_ACCOUNT_ID = accountupdateapi_dto.useraccountid#GeninusClientScript 1318
		PREFECTURE_CODE = accountupdateapi_dto.prefecturecode#GeninusClientScript 1318
		SHOKOKAI_CD = accountupdateapi_dto.shokokaicd#GeninusClientScript 1318
		USER_ID = accountupdateapi_dto.userid#GeninusClientScript 1318
		SHOKUIN_KJ = accountupdateapi_dto.shokuinkj#GeninusClientScript 1318
		EMAIL = accountupdateapi_dto.email#GeninusClientScript 1318
		PASSWORD = accountupdateapi_dto.password#GeninusClientScript 1318
		PERMISSION_LEVEL = accountupdateapi_dto.permissionlevel#GeninusClientScript 1318
		STATUS = accountupdateapi_dto.status#GeninusClientScript 1318
		QUALIFICATION_CODES = getattr(accountupdateapi_dto, "qualificationcodes", "")
		api132_updateaccount = Api132UpdateaccountDto.dict_to_json({}) #CommonFunction 110
		KOUSHINKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント編集画面登録ボタン_AccountUpdateAPI_(API)
			
			#「項目処理」（共通関数:AccountUpdateAPI）,パラメータは（user_account_id,prefecture_code,shokokai_cd,user_id,shokuin_kj,email,password,permission_level,status）
			
			#以下の処理を行う。
			
			#関数「API132_UpdateAccount」の「db_API132_UpdateAccount」メソッドを行う,パラメータは「prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,permission_level,password,user_account_id」。

			if find_live_account_id(PREFECTURE_CODE, USER_ID, exclude_user_account_id=USER_ACCOUNT_ID):
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "このユーザIDは既に使用されています")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				return
			
			# prefecture_code
			api132_updateaccount.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api132_updateaccount.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# user_id
			api132_updateaccount.userid = USER_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokuin_kj
			api132_updateaccount.shokuinkj = SHOKUIN_KJ #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# email
			api132_updateaccount.email = EMAIL #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# status
			api132_updateaccount.status = STATUS if STATUS not in (None, "") else 1 #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# permission_level
			api132_updateaccount.permissionlevel = PERMISSION_LEVEL #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# password（空欄なら変更しない）
			if PASSWORD not in (None, ""):
				api132_updateaccount.password = encrypt_for_storage(PASSWORD)
			else:
				api132_updateaccount.password = ""
			#ArgumentGenerator 274
			
			# user_account_id
			api132_updateaccount.useraccountid = USER_ACCOUNT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			api132_updateaccountlistVar = Api132UpdateaccountDao().api132_updateaccount(api132_updateaccount) #ResultGenerator 104
			#ResultGenerator 104
			if api132_updateaccountlistVar != None and len(api132_updateaccountlistVar) > 0 :
				KOUSHINKENSUU = "1"
			#<更新件数>が"1"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if KOUSHINKENSUU.replace(" ", "") == "1" : #GeniusContion 823
				#GeniusContion 823
				replace_account_qualifications(USER_ACCOUNT_ID, QUALIFICATION_CODES)
				#「更新しました」メッセージを表示する。
				jsonObj.setValue(utils.json_constant.JSONID_MSG, "更新しました")
				#処理終了。
				pass
				#GeniusClientScript 1207
			else:
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "更新に失敗しました")
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
