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
from app.dao.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_dao import Api143GetknowledgeentrydetailDao
from app.dao.api147_getentrythemes.api147_getentrythemes_dao import Api147GetentrythemesDao
from app.dto.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_dto import Api143GetknowledgeentrydetailDto
from app.dto.api147_getentrythemes.api147_getentrythemes_dto import Api147GetentrythemesDto
from app.dto.entrydetailinitapi.entrydetailinitapi_dto import EntrydetailinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntrydetailinitapiService :

	#	# 
	# 知識データ詳細画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entrydetailinitapi(self,entrydetailinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		KNOWLEDGE_ENTRY_ID = entrydetailinitapi_dto.knowledgeentryid#GeninusClientScript 1318
		api143_getknowledgeentrydetail = Api143GetknowledgeentrydetailDto.dict_to_json({}) #CommonFunction 110
		api143_getknowledgeentrydetailList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api143_getknowledgeentrydetail_dto = None #ResultGenerator 119
		#ResultGenerator365
		KNOWLEDGEENTRYID = ""
		KNOWLEDGECODE = ""
		TITLE = ""
		KNOWLEDGEDOCUMENTID = ""
		DOCUMENTTITLE = ""
		UPDATEDDATE = ""
		STATUS = ""
		CONTENT = ""
		api147_getentrythemes = Api147GetentrythemesDto.dict_to_json({}) #CommonFunction 110
		api147_getentrythemesList = None #ResultGenerator 72
		#_dto api147_getentrythemes_dto = None #ResultGenerator 119
		THEMEID = ""
		THEMECODE = ""
		LABEL = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ詳細画面初期表示_EntryDetailInitAPI_(API)
			
			#「項目処理」（共通関数:EntryDetailInitAPI）,パラメータは（knowledge_entry_id）
			
			#以下の処理を行う。
			
			#関数「API143_GetKnowledgeEntryDetail」の「db_API143_GetKnowledgeEntryDetail」メソッドを行う,パラメータは「knowledge_entry_id」,戻り値設定は「<knowledge_entry_id>=knowledge_entry_id,<knowledge_code>=knowledge_code,<title>=title,<knowledge_document_id>=knowledge_document_id,<document_title>=document_title,<updated_date>=updated_date,<status>=status,<content>=content」を設定する。
			
			# knowledge_entry_id
			api143_getknowledgeentrydetail.knowledgeentryid = KNOWLEDGE_ENTRY_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api143_getknowledgeentrydetailList = Api143GetknowledgeentrydetailDao().api143_getknowledgeentrydetail(api143_getknowledgeentrydetail)
			api143_getknowledgeentrydetaillistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api143_getknowledgeentrydetailList != None :
				api143_getknowledgeentrydetaillistVar = api143_getknowledgeentrydetailList.fetchall() if hasattr(api143_getknowledgeentrydetailList, 'fetchall') else api143_getknowledgeentrydetailList
			if api143_getknowledgeentrydetaillistVar != None and len(api143_getknowledgeentrydetaillistVar) > 0 :
				SHUTOKUKENSUU = str(len(api143_getknowledgeentrydetaillistVar))
			# --LINE114 retrieved first value
			if api143_getknowledgeentrydetaillistVar != None and len(api143_getknowledgeentrydetaillistVar) > 0 :
				rec = api143_getknowledgeentrydetaillistVar[0]
				KNOWLEDGEENTRYID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_entry_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				KNOWLEDGECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				TITLE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title")) # ResultGenerator 385
				# ResultGenerator 385
				
				KNOWLEDGEDOCUMENTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				DOCUMENTTITLE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "document_title")) # ResultGenerator 385
				# ResultGenerator 385
				
				UPDATEDDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "updated_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				STATUS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status")) # ResultGenerator 385
				# ResultGenerator 385
				
				CONTENT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API147_GetEntryThemes」の「db_API147_GetEntryThemes」メソッドを行う,パラメータは「knowledge_entry_id」,戻り値設定は「<theme_id>=theme_id,<theme_code>=theme_code,<label>=label」を設定する。
			
			# knowledge_entry_id
			api147_getentrythemes.knowledgeentryid = KNOWLEDGEENTRYID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api147_getentrythemesList = Api147GetentrythemesDao().api147_getentrythemes(api147_getentrythemes)
			api147_getentrythemeslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api147_getentrythemesList != None :
				api147_getentrythemeslistVar = api147_getentrythemesList.fetchall() if hasattr(api147_getentrythemesList, 'fetchall') else api147_getentrythemesList
			if api147_getentrythemeslistVar != None and len(api147_getentrythemeslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api147_getentrythemeslistVar))
			# --LINE114 retrieved first value
			if api147_getentrythemeslistVar != None and len(api147_getentrythemeslistVar) > 0 :
				rec = api147_getentrythemeslistVar[0]
				THEMEID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				LABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
