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
from app.dao.api132_updateaccount.api132_updateaccount_dao import Api132UpdateaccountDao
from app.dto.accountupdateapi.accountupdateapi_dto import AccountupdateapiDto
from app.dto.api132_updateaccount.api132_updateaccount_dto import Api132UpdateaccountDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




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
		api132_updateaccount = Api132UpdateaccountDto.dict_to_json({}) #CommonFunction 110
		KOUSHINKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント編集画面登録ボタン_AccountUpdateAPI_(API)
			
			#「項目処理」（共通関数:AccountUpdateAPI）,パラメータは（user_account_id,prefecture_code,shokokai_cd,user_id,shokuin_kj,email,password,permission_level,status）
			
			#以下の処理を行う。
			
			#関数「API132_UpdateAccount」の「db_API132_UpdateAccount」メソッドを行う,パラメータは「prefecture_code,shokokai_cd,user_id,shokuin_kj,email,status,permission_level,password,user_account_id」。
			
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
			api132_updateaccount.status = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# permission_level
			api132_updateaccount.permissionlevel = PERMISSION_LEVEL #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# password
			api132_updateaccount.password = PASSWORD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# user_account_id
			api132_updateaccount.useraccountid = USER_ACCOUNT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			Api132UpdateaccountDao().api132_updateaccount(api132_updateaccount) #ResultGenerator 104
			#ResultGenerator 104
			#<更新件数>が"1"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if KOUSHINKENSUU.replace(" ", "") == "1" : #GeniusContion 823
				#GeniusContion 823
				#「更新しました」メッセージを表示する。
				jsonObj.setScript(utils.json_constant.JSONID_MSG, "更新しました")
				#処理終了。
				pass
				#GeniusClientScript 1207
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
