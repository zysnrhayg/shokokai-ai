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
from app.dao.api145_updateknowledgeentry.api145_updateknowledgeentry_dao import Api145UpdateknowledgeentryDao
from app.dto.api145_updateknowledgeentry.api145_updateknowledgeentry_dto import Api145UpdateknowledgeentryDto
from app.dto.entryupdateapi.entryupdateapi_dto import EntryupdateapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntryupdateapiService :

	#	# 
	# 知識データ編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entryupdateapi(self,entryupdateapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		KNOWLEDGE_ENTRY_ID = entryupdateapi_dto.knowledgeentryid#GeninusClientScript 1318
		TITLE = entryupdateapi_dto.title#GeninusClientScript 1318
		KNOWLEDGE_DOCUMENT_ID = entryupdateapi_dto.knowledgedocumentid#GeninusClientScript 1318
		CONTENT = entryupdateapi_dto.content#GeninusClientScript 1318
		THEME_IDS = entryupdateapi_dto.themeids#GeninusClientScript 1318
		STATUS = entryupdateapi_dto.status#GeninusClientScript 1318
		api145_updateknowledgeentry = Api145UpdateknowledgeentryDto.dict_to_json({}) #CommonFunction 110
		KOUSHINKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ編集画面登録ボタン_EntryUpdateAPI_(API)
			
			#「項目処理」（共通関数:EntryUpdateAPI）,パラメータは（knowledge_entry_id,title,knowledge_document_id,content,theme_ids,status）
			
			#以下の処理を行う。
			
			#関数「API145_UpdateKnowledgeEntry」の「db_API145_UpdateKnowledgeEntry」メソッドを行う,パラメータは「title,knowledge_document_id,status,content,knowledge_entry_id」。
			
			# title
			api145_updateknowledgeentry.title = TITLE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api145_updateknowledgeentry.prefecturecode = KNOWLEDGE_DOCUMENT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# theme
			api145_updateknowledgeentry.theme = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# knowledge_document_id
			api145_updateknowledgeentry.knowledgedocumentid = CONTENT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# status
			api145_updateknowledgeentry.status = KNOWLEDGE_ENTRY_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# body
			api145_updateknowledgeentry.body = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# updated_by
			api145_updateknowledgeentry.updatedby = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# knowledge_entry_id
			api145_updateknowledgeentry.knowledgeentryid = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			Api145UpdateknowledgeentryDao().api145_updateknowledgeentry(api145_updateknowledgeentry) #ResultGenerator 104
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
		
			
	
	
