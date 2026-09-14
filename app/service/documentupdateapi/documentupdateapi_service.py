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
from app.dao.api139_updateknowledgedocument.api139_updateknowledgedocument_dao import Api139UpdateknowledgedocumentDao
from app.dao.api_knowledgedocumentversioninformation.api_knowledgedocumentversioninformation_dao import ApiKnowledgedocumentversioninformationDao
from app.dto.api139_updateknowledgedocument.api139_updateknowledgedocument_dto import Api139UpdateknowledgedocumentDto
from app.dto.api_knowledgedocumentversioninformation.api_knowledgedocumentversioninformation_dto import ApiKnowledgedocumentversioninformationDto
from app.dto.documentupdateapi.documentupdateapi_dto import DocumentupdateapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DocumentupdateapiService :

	#	# 
	# ナレッジ文書編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentupdateapi(self,documentupdateapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		KNOWLEDGE_DOCUMENT_ID = documentupdateapi_dto.knowledgedocumentid#GeninusClientScript 1318
		TITLE = documentupdateapi_dto.title#GeninusClientScript 1318
		CATEGORY = documentupdateapi_dto.category#GeninusClientScript 1318
		FORMAT = documentupdateapi_dto.format#GeninusClientScript 1318
		api139_updateknowledgedocument = Api139UpdateknowledgedocumentDto.dict_to_json({}) #CommonFunction 110
		api_knowledgedocumentversioninformation = ApiKnowledgedocumentversioninformationDto.dict_to_json({}) #CommonFunction 110
		KOUSHINKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書編集画面登録ボタン_DocumentUpdateAPI_(API)
			
			#「項目処理」（共通関数:DocumentUpdateAPI）,パラメータは（knowledge_document_id,title,category,format）
			
			#以下の処理を行う。
			
			#関数「API139_UpdateKnowledgeDocument」の「db_API139_UpdateKnowledgeDocument」メソッドを行う,パラメータは「title,category,format,knowledge_document_id」。
			
			# title
			api139_updateknowledgedocument.title = TITLE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api139_updateknowledgedocument.prefecturecode = CATEGORY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# category
			api139_updateknowledgedocument.category = FORMAT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# format
			api139_updateknowledgedocument.format = KNOWLEDGE_DOCUMENT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# updated_by
			api139_updateknowledgedocument.updatedby = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# knowledge_document_id
			api139_updateknowledgedocument.knowledgedocumentid = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			Api139UpdateknowledgedocumentDao().api139_updateknowledgedocument(api139_updateknowledgedocument) #ResultGenerator 104
			#ResultGenerator 104
			#関数「API_KnowledgeDocumentVersionInformation」の「db_API_KnowledgeDocumentVersionInformation」メソッドを行う,パラメータは「title,category,format,knowledge_document_id」。
			
			# status
			api_knowledgedocumentversioninformation.status = TITLE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# updated_by
			api_knowledgedocumentversioninformation.updatedby = CATEGORY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# knowledge_document_id
			api_knowledgedocumentversioninformation.knowledgedocumentid = FORMAT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			ApiKnowledgedocumentversioninformationDao().api_knowledgedocumentversioninformation(api_knowledgedocumentversioninformation) #ResultGenerator 104
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
		
			
	
	
