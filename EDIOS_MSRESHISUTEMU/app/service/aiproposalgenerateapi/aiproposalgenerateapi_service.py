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
from app.dto.aiproposalgenerateapi.aiproposalgenerateapi_dto import AiproposalgenerateapiDto
from app.dto.api154_getpublishedentries.api154_getpublishedentries_dto import Api154GetpublishedentriesDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AiproposalgenerateapiService :

	#	# 
	# AI支援提案AI提案を生成
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aiproposalgenerateapi(self,aiproposalgenerateapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		INDUSTRY = aiproposalgenerateapi_dto.industry#GeninusClientScript 1318
		THEME_FILTER_GROUP = aiproposalgenerateapi_dto.themefiltergroup#GeninusClientScript 1318
		CONSULTATION_SUMMARY = aiproposalgenerateapi_dto.consultationsummary#GeninusClientScript 1318
		api154_getpublishedentries = Api154GetpublishedentriesDto.dict_to_json({}) #CommonFunction 110
		api154_getpublishedentriesList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api154_getpublishedentries_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#AI支援提案AI提案を生成_AIPROPOSALGENERATEAPI_(API)
			
			#「項目処理」（共通関数:AIPROPOSALGENERATEAPI）,パラメータは（industry,theme_filter_group,consultation_summary）
			
			#以下の処理を行う。
			
			#方法:POST/EV_AI_PROPOSAL_GENERATE.do（Content-Type:application/json）。op_id=search.generate
			
			#入力JSON:industry,theme_filter_group,consultation_summary
			
			#項目処理【AI提案を生成】:埋め込みJSON+定型テンプレートで描画。実AIなし
			
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
			#proposals[]またはresults[]を返す。
			proposals = []
			results = []
			if api154_getpublishedentrieslistVar != None and len(api154_getpublishedentrieslistVar) > 0 :
				for entity in api154_getpublishedentrieslistVar :
					if isinstance(entity, dict) :
						item = entity
					else :
						item = dict(entity) if entity is not None else {}
					proposals.append(item)
					results.append(item)
			jsonObj.setValue("proposals", proposals)
			jsonObj.setValue("results", results)
			#処理が失敗した場合,JSON「e」にエラーメッセージを設定し処理終了。
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
