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
from app.dao.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_dao import ApiIchiranteburushiborikomiDao
from app.dto.accountsfilterapi.accountsfilterapi_dto import AccountsfilterapiDto
from app.dto.api_ichiranteburushiborikomi.api_ichiranteburushiborikomi_dto import ApiIchiranteburushiborikomiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AccountsfilterapiService :

	#	# 
	# アカウント一覧一覧絞込（県/商工会/権限/検索）
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accountsfilterapi(self,accountsfilterapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		PREFECTURE_CODE = accountsfilterapi_dto.prefecturecode#GeninusClientScript 1318
		SHOKOKAI_CD = accountsfilterapi_dto.shokokaicd#GeninusClientScript 1318
		PERMISSION_LEVEL = accountsfilterapi_dto.permissionlevel#GeninusClientScript 1318
		STATUS = accountsfilterapi_dto.status#GeninusClientScript 1318
		CORE_LINKED = accountsfilterapi_dto.corelinked#GeninusClientScript 1318
		KEYWORD = accountsfilterapi_dto.keyword#GeninusClientScript 1318
		api_ichiranteburushiborikomi = ApiIchiranteburushiborikomiDto.dict_to_json({}) #CommonFunction 110
		api_ichiranteburushiborikomiList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api_ichiranteburushiborikomi_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント一覧一覧絞込（県/商工会/権限/検索）_AccountsFilterAPI_(API)
			
			#「項目処理」（共通関数:AccountsFilterAPI）,パラメータは（prefecture_code,shokokai_cd,permission_level,status,core_linked,keyword）
			
			#以下の処理を行う。
			
			#関数「API_IchiranTeburuShiborikomi」の「db_API_IchiranTeburuShiborikomi」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「」を設定する。
			
			# mst_user_account.prefecture_code
			api_ichiranteburushiborikomi.mstuseraccountprefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# mst_user_account.shokokai_cd
			api_ichiranteburushiborikomi.mstuseraccountshokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
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
		
			
	
	
