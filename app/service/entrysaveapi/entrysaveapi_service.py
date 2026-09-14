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
from app.dao.api144_insertknowledgeentry.api144_insertknowledgeentry_dao import Api144InsertknowledgeentryDao
from app.dto.api144_insertknowledgeentry.api144_insertknowledgeentry_dto import Api144InsertknowledgeentryDto
from app.dto.entrysaveapi.entrysaveapi_dto import EntrysaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntrysaveapiService :

	#	# 
	# 知識データ新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entrysaveapi(self,entrysaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		TITLE = entrysaveapi_dto.title#GeninusClientScript 1318
		KNOWLEDGE_DOCUMENT_ID = entrysaveapi_dto.knowledgedocumentid#GeninusClientScript 1318
		CONTENT = entrysaveapi_dto.content#GeninusClientScript 1318
		THEME_IDS = entrysaveapi_dto.themeids#GeninusClientScript 1318
		STATUS = entrysaveapi_dto.status#GeninusClientScript 1318
		api144_insertknowledgeentry = Api144InsertknowledgeentryDto.dict_to_json({}) #CommonFunction 110
		TOUROKUKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ新規画面登録ボタン_EntrySaveAPI_(API)
			
			#「項目処理」（共通関数:EntrySaveAPI）,パラメータは（title,knowledge_document_id,content,theme_ids,status）
			
			#以下の処理を行う。
			
			#関数「API144_InsertKnowledgeEntry」の「db_API144_InsertKnowledgeEntry」メソッドを行う,パラメータは「knowledge_code,title,knowledge_document_id,status,content,prefecture_code」。
			
			# knowledge_entry_id
			api144_insertknowledgeentry.knowledgeentryid = KNOWLEDGE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# knowledge_code
			api144_insertknowledgeentry.knowledgecode = TITLE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# title
			api144_insertknowledgeentry.title = KNOWLEDGE_DOCUMENT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api144_insertknowledgeentry.prefecturecode = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# theme
			api144_insertknowledgeentry.theme = CONTENT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# knowledge_document_id
			api144_insertknowledgeentry.knowledgedocumentid = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# status
			api144_insertknowledgeentry.status = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# body
			api144_insertknowledgeentry.body = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# created_by
			api144_insertknowledgeentry.createdby = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# updated_by
			api144_insertknowledgeentry.updatedby = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			Api144InsertknowledgeentryDao().api144_insertknowledgeentry(api144_insertknowledgeentry) #ResultGenerator 104
			#ResultGenerator 104
			#<登録件数>が"1"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if TOUROKUKENSUU.replace(" ", "") == "1" : #GeniusContion 823
				#GeniusContion 823
				#「登録しました」メッセージを表示する。
				jsonObj.setScript(utils.json_constant.JSONID_MSG, "登録しました")
				#処理終了。
				pass
				#GeniusClientScript 1207
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
