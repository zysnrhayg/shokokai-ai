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
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api154_getpublishedentries.api154_getpublishedentries_dao import Api154GetpublishedentriesDao
from app.dto.aiproposalinitapi.aiproposalinitapi_dto import AiproposalinitapiDto
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api154_getpublishedentries.api154_getpublishedentries_dto import Api154GetpublishedentriesDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AiproposalinitapiService :

	#	# 
	# AI支援提案画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aiproposalinitapi(self,aiproposalinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		KNOWLEDGE_ENTRY_ID = aiproposalinitapi_dto.knowledgeentryid#GeninusClientScript 1318
		TITLE = aiproposalinitapi_dto.title#GeninusClientScript 1318
		CONTENT = aiproposalinitapi_dto.content#GeninusClientScript 1318
		THEME_LABEL = aiproposalinitapi_dto.themelabel#GeninusClientScript 1318
		DOCUMENT_VERSION = aiproposalinitapi_dto.documentversion#GeninusClientScript 1318
		FISCAL_YEAR_ID = aiproposalinitapi_dto.fiscalyearid#GeninusClientScript 1318
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
		api120_getthemes = Api120GetthemesDto.dict_to_json({}) #CommonFunction 110
		api120_getthemesList = None #ResultGenerator 72
		#_dto api120_getthemes_dto = None #ResultGenerator 119
		THEMEID = ""
		THEMECODE = ""
		LABEL = ""
		FILTERGROUP = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#AI支援提案画面初期表示_AiProposalInitAPI_(API)
			
			#「項目処理」（共通関数:AiProposalInitAPI）,パラメータは（knowledge_entry_id,title,content,theme_label,document_version,fiscal_year_id）
			
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
				
			#関数「API120_GetThemes」の「db_API120_GetThemes」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<theme_id>=theme_id,<theme_code>=theme_code,<label>=label,<filter_group>=filter_group」を設定する。
			
			# fiscal_year_id
			api120_getthemes.fiscalyearid = FISCAL_YEAR_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api120_getthemesList = Api120GetthemesDao().api120_getthemes(api120_getthemes)
			api120_getthemeslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api120_getthemesList != None :
				api120_getthemeslistVar = api120_getthemesList.fetchall() if hasattr(api120_getthemesList, 'fetchall') else api120_getthemesList
			if api120_getthemeslistVar != None and len(api120_getthemeslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api120_getthemeslistVar))
			# --LINE114 retrieved first value
			if api120_getthemeslistVar != None and len(api120_getthemeslistVar) > 0 :
				rec = api120_getthemeslistVar[0]
				THEMEID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				LABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")) # ResultGenerator 385
				# ResultGenerator 385
				
				FILTERGROUP = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "filter_group")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
