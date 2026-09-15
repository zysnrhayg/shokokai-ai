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
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dao.api102_getshokokai.api102_getshokokai_dao import Api102GetshokokaiDao
from app.dao.api103_getaccountdetail.api103_getaccountdetail_dao import Api103GetaccountdetailDao
from app.dto.accounteditinitapi.accounteditinitapi_dto import AccounteditinitapiDto
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto
from app.dto.api102_getshokokai.api102_getshokokai_dto import Api102GetshokokaiDto
from app.dto.api103_getaccountdetail.api103_getaccountdetail_dto import Api103GetaccountdetailDto
from app.common.account_json import put_account_on_json
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AccounteditinitapiService :

	#	# 
	# アカウント編集画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accounteditinitapi(self,accounteditinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		USER_ACCOUNT_ID = accounteditinitapi_dto.useraccountid#GeninusClientScript 1318
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
		api100_getprefecturenames = Api100GetprefecturenamesDto.dict_to_json({}) #CommonFunction 110
		api100_getprefecturenamesList = None #ResultGenerator 72
		#_dto api100_getprefecturenames_dto = None #ResultGenerator 119
		NAME = ""
		SHORTNAME = ""
		REGION = ""
		SORTORDER = ""
		ISPSEUDO = ""
		api102_getshokokai = Api102GetshokokaiDto.dict_to_json({}) #CommonFunction 110
		api102_getshokokaiList = None #ResultGenerator 72
		#_dto api102_getshokokai_dto = None #ResultGenerator 119
		ONLY_FEDERATION = ""
		EXCLUDE_FEDERATION = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント編集画面初期表示_AccountEditInitAPI_(API)
			
			#「項目処理」（共通関数:AccountEditInitAPI）,パラメータは（user_account_id）
			
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
				account_prefecture_code = PREFECTURECODE
			else:
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "アカウントが見つかりません")
				account_prefecture_code = ""
			#関数「API100_GetPrefectureNames」の「db_API100_GetPrefectureNames」メソッドを行う,パラメータは「」,戻り値設定は「<prefecture_code>=prefecture_code,<name>=name,<short_name>=short_name,<region>=region,<sort_order>=sort_order,<is_pseudo>=is_pseudo」を設定する。
			
			#ReulstGenerator 87
			api100_getprefecturenamesList = Api100GetprefecturenamesDao().api100_getprefecturenames(api100_getprefecturenames)
			api100_getprefecturenameslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api100_getprefecturenamesList != None :
				api100_getprefecturenameslistVar = api100_getprefecturenamesList.fetchall() if hasattr(api100_getprefecturenamesList, 'fetchall') else api100_getprefecturenamesList
			if api100_getprefecturenameslistVar != None and len(api100_getprefecturenameslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api100_getprefecturenameslistVar))
			# --LINE114 retrieved first value
			if api100_getprefecturenameslistVar != None and len(api100_getprefecturenameslistVar) > 0 :
				rec = api100_getprefecturenameslistVar[0]
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHORTNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "short_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				REGION = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "region")) # ResultGenerator 385
				# ResultGenerator 385
				
				SORTORDER = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "sort_order")) # ResultGenerator 385
				# ResultGenerator 385
				
				ISPSEUDO = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "is_pseudo")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API102_GetShokokai」の「db_API102_GetShokokai」メソッドを行う,パラメータは「prefecture_code,only_federation,exclude_federation」,戻り値設定は「<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<name>=name」を設定する。
			
			# prefecture_code
			api102_getshokokai.prefecturecode = account_prefecture_code #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# only_federation
			api102_getshokokai.onlyfederation = ONLY_FEDERATION #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# exclude_federation
			api102_getshokokai.excludefederation = EXCLUDE_FEDERATION #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api102_getshokokaiList = Api102GetshokokaiDao().api102_getshokokai(api102_getshokokai)
			api102_getshokokailistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api102_getshokokaiList != None :
				api102_getshokokailistVar = api102_getshokokaiList.fetchall() if hasattr(api102_getshokokaiList, 'fetchall') else api102_getshokokaiList
			if api102_getshokokailistVar != None and len(api102_getshokokailistVar) > 0 :
				SHUTOKUKENSUU = str(len(api102_getshokokailistVar))
			# --LINE114 retrieved first value
			if api102_getshokokailistVar != None and len(api102_getshokokailistVar) > 0 :
				rec = api102_getshokokailistVar[0]
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
