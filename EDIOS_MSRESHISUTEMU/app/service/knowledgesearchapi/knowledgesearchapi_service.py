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
		KEYWORD = knowledgesearchapi_dto.keyword#GeninusClientScript 1318
		api154_getpublishedentries = Api154GetpublishedentriesDto.dict_to_json({}) #CommonFunction 110
		api154_getpublishedentriesList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api154_getpublishedentries_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#AI支援提案ナレッジを検索_KNOWLEDGESEARCHAPI_(API)
			
			#「項目処理」（共通関数:KNOWLEDGESEARCHAPI）,パラメータは（keyword）
			
			#以下の処理を行う。
			
			#関数「API154_GetPublishedEntries」の「db_API154_GetPublishedEntries」メソッドを行う,パラメータは「」,戻り値設定は「」。
			
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
			#関数「API154_GetPublishedEntries」の「db_API154_GetPublishedEntries」取得結果をJSON形式でGrid「rows」に設定し,20行で改ページする。
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
		
			
	
	
