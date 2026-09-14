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
from app.dao.api147_getentrythemes.api147_getentrythemes_dao import Api147GetentrythemesDao
from app.dao.api175_entryforminit.api175_entryforminit_dao import Api175EntryforminitDao
from app.dto.api147_getentrythemes.api147_getentrythemes_dto import Api147GetentrythemesDto
from app.dto.api175_entryforminit.api175_entryforminit_dto import Api175EntryforminitDto
from app.dto.entryformnewinitapi.entryformnewinitapi_dto import EntryformnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntryformnewinitapiService :

	#	# 
	# 知識データ新規＋ 知識データを登録
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entryformnewinitapi(self,entryformnewinitapi_dto,jsonObj) :
			
		api175_entryforminit = Api175EntryforminitDto.dict_to_json({}) #CommonFunction 110
		api175_entryforminitList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api175_entryforminit_dto = None #ResultGenerator 119
		#ResultGenerator365
		DOCUMENTCODE = ""
		TITLE = ""
		api147_getentrythemes = Api147GetentrythemesDto.dict_to_json({}) #CommonFunction 110
		api147_getentrythemesList = None #ResultGenerator 72
		#_dto api147_getentrythemes_dto = None #ResultGenerator 119
		THEMEID = ""
		THEMECODE = ""
		LABEL = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ新規＋ 知識データを登録_EntryFormNewInitAPI_(API)
			
			#「項目処理」（共通関数:EntryFormNewInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API175_EntryFormInit」の「db_API175_EntryFormInit」メソッドを行う,パラメータは「」,戻り値設定は「<document_code>=document_code,<title>=title」を設定する。
			
			#ReulstGenerator 87
			api175_entryforminitList = Api175EntryforminitDao().api175_entryforminit(api175_entryforminit)
			api175_entryforminitlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api175_entryforminitList != None :
				api175_entryforminitlistVar = api175_entryforminitList.fetchall() if hasattr(api175_entryforminitList, 'fetchall') else api175_entryforminitList
			if api175_entryforminitlistVar != None and len(api175_entryforminitlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api175_entryforminitlistVar))
			# --LINE114 retrieved first value
			if api175_entryforminitlistVar != None and len(api175_entryforminitlistVar) > 0 :
				rec = api175_entryforminitlistVar[0]
				DOCUMENTCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "document_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				TITLE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API147_GetEntryThemes」の「db_API147_GetEntryThemes」メソッドを行う,パラメータは「knowledge_entry_id」,戻り値設定は「<theme_id>=theme_id,<theme_code>=theme_code,<label>=label」を設定する。
			
			# knowledge_entry_id
			api147_getentrythemes.knowledgeentryid = KNOWLEDGE_ENTRY_ID #ArgumentGenerator 274
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
		
			
	
	
