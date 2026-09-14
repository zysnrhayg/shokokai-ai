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
from app.dao.api102_getshokokai.api102_getshokokai_dao import Api102GetshokokaiDao
from app.dao.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_dao import ApiIchiranteburushiborikomiDao
from app.dto.accountsinitapi.accountsinitapi_dto import AccountsinitapiDto
from app.dto.api102_getshokokai.api102_getshokokai_dto import Api102GetshokokaiDto
from app.dto.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_dto import ApiIchiranteburushiborikomiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AccountsinitapiService :

	#	# 
	# アカウント一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accountsinitapi(self,accountsinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		PREFECTURE_CODE = accountsinitapi_dto.prefecturecode#GeninusClientScript 1318
		ONLY_FEDERATION = accountsinitapi_dto.onlyfederation#GeninusClientScript 1318
		EXCLUDE_FEDERATION = accountsinitapi_dto.excludefederation#GeninusClientScript 1318
		ROLE_CODE = accountsinitapi_dto.rolecode#GeninusClientScript 1318
		SHOKOKAI_CD = accountsinitapi_dto.shokokaicd#GeninusClientScript 1318
		FEDERATION_CD = accountsinitapi_dto.federationcd#GeninusClientScript 1318
		api102_getshokokai = Api102GetshokokaiDto.dict_to_json({}) #CommonFunction 110
		api102_getshokokaiList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api102_getshokokai_dto = None #ResultGenerator 119
		#ResultGenerator365
		PREFECTURECODE = ""
		SHOKOKAICD = ""
		NAME = ""
		api_ichiranteburushiborikomi = ApiIchiranteburushiborikomiDto.dict_to_json({}) #CommonFunction 110
		api_ichiranteburushiborikomiList = None #ResultGenerator 72
		#_dto api_ichiranteburushiborikomi_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント一覧画面初期表示_AccountsInitAPI_(API)
			
			#「項目処理」（共通関数:AccountsInitAPI）,パラメータは（prefecture_code,only_federation,exclude_federation,role_code,shokokai_cd,federation_cd）
			
			#以下の処理を行う。
			
			#関数「API102_GetShokokai」の「db_API102_GetShokokai」メソッドを行う,パラメータは「prefecture_code,only_federation,exclude_federation」,戻り値設定は「<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<name>=name」を設定する。
			
			# prefecture_code
			api102_getshokokai.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
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
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAICD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")) # ResultGenerator 385
				# ResultGenerator 385
				
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API_IchiranTeburuShiborikomi」の「db_API_IchiranTeburuShiborikomi」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「」を設定する。
			
			# mst_user_account.prefecture_code
			api_ichiranteburushiborikomi.mstuseraccountprefecturecode = PREFECTURECODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# mst_user_account.shokokai_cd
			api_ichiranteburushiborikomi.mstuseraccountshokokaicd = SHOKOKAICD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# LIMIT
			api_ichiranteburushiborikomi.limit = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# OFFSET
			api_ichiranteburushiborikomi.offset = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			#ReulstGenerator 87
			api_ichiranteburushiborikomiList = ApiIchiranteburushiborikomiDao().api_ichiranteburushiborikomi(api_ichiranteburushiborikomi)
			api_ichiranteburushiborikomilistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_ichiranteburushiborikomiList != None :
				api_ichiranteburushiborikomilistVar = api_ichiranteburushiborikomiList.fetchall() if hasattr(api_ichiranteburushiborikomiList, 'fetchall') else api_ichiranteburushiborikomiList
			if api_ichiranteburushiborikomilistVar != None and len(api_ichiranteburushiborikomilistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_ichiranteburushiborikomilistVar))
			# --LINE114 retrieved first value
			if api_ichiranteburushiborikomilistVar != None and len(api_ichiranteburushiborikomilistVar) > 0 :
				rec = api_ichiranteburushiborikomilistVar[0]
			#関数「API_IchiranTeburuShiborikomi」の「db_API_IchiranTeburuShiborikomi」取得結果をJSON形式でGrid「rows」に設定し,20行で改ページする。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api_ichiranteburushiborikomilistVar != None and len(api_ichiranteburushiborikomilistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_ichiranteburushiborikomilistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_ichiranteburushiborikomilistVar[i]
					selMap ={} #GeniusGrid681
					#GeniusGrid681
					mapList.insert(len(mapList),selMap)
			result = json.dumps(mapList, ensure_ascii=False)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
