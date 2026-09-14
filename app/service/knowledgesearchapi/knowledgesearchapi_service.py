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
from app.dao.api154_getpublishedentries.api154_getpublishedentries_dao import Api154GetpublishedentriesDao
from app.dto.api154_getpublishedentries.api154_getpublishedentries_dto import Api154GetpublishedentriesDto
from app.dto.knowledgesearchapi.knowledgesearchapi_dto import KnowledgesearchapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class KnowledgesearchapiService :

	#	# 
	# AI支援提案ナレッジを検索
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def knowledgesearchapi(self,knowledgesearchapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		KNOWLEDGE_ENTRY_ID = knowledgesearchapi_dto.knowledgeentryid#GeninusClientScript 1318
		TITLE = knowledgesearchapi_dto.title#GeninusClientScript 1318
		CONTENT = knowledgesearchapi_dto.content#GeninusClientScript 1318
		THEME_LABEL = knowledgesearchapi_dto.themelabel#GeninusClientScript 1318
		DOCUMENT_VERSION = knowledgesearchapi_dto.documentversion#GeninusClientScript 1318
		api154_getpublishedentries = Api154GetpublishedentriesDto.dict_to_json({}) #CommonFunction 110
		api154_getpublishedentriesList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api154_getpublishedentries_dto = None #ResultGenerator 119
		#ResultGenerator365
		KNOWLEDGEENTRYID = ""
		KNOWLEDGECODE = ""
		UPDATEDDATE = ""
		KNOWLEDGEDOCUMENTID = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#AI支援提案ナレッジを検索_KNOWLEDGESEARCHAPI_(API)
			
			#「項目処理」（共通関数:KNOWLEDGESEARCHAPI）,パラメータは（knowledge_entry_id,title,content,theme_label,document_version）
			
			#以下の処理を行う。
			
			#関数「API154_GetPublishedEntries」の「db_API154_GetPublishedEntries」メソッドを行う,パラメータは「keyword,prefecture_code」,戻り値設定は「<knowledge_entry_id>=knowledge_entry_id,<knowledge_code>=knowledge_code,<title>=title,<content>=content,<updated_date>=updated_date,<knowledge_document_id>=knowledge_document_id」を設定する。
			
			# keyword
			api154_getpublishedentries.keyword = KEYWORD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api154_getpublishedentries.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api154_getpublishedentriesList = Api154GetpublishedentriesDao().api154_getpublishedentries(api154_getpublishedentries)
			api154_getpublishedentrieslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api154_getpublishedentriesList != None :
				api154_getpublishedentrieslistVar = api154_getpublishedentriesList.fetchall() if hasattr(api154_getpublishedentriesList, 'fetchall') else api154_getpublishedentriesList
			if api154_getpublishedentrieslistVar != None and len(api154_getpublishedentrieslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api154_getpublishedentrieslistVar))
			# --LINE114 retrieved first value
			if api154_getpublishedentrieslistVar != None and len(api154_getpublishedentrieslistVar) > 0 :
				rec = api154_getpublishedentrieslistVar[0]
				KNOWLEDGEENTRYID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_entry_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				KNOWLEDGECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				TITLE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title")) # ResultGenerator 385
				# ResultGenerator 385
				
				CONTENT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content")) # ResultGenerator 385
				# ResultGenerator 385
				
				UPDATEDDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "updated_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				KNOWLEDGEDOCUMENTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API154_GetPublishedEntries」の「db_API154_GetPublishedEntries」取得結果をGrid「ks-results」に設定する。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api154_getpublishedentrieslistVar != None and len(api154_getpublishedentrieslistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api154_getpublishedentrieslistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api154_getpublishedentrieslistVar[i]
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
		
			
	
	
