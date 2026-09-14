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
from app.dao.api137_insertknowledgedocument.api137_insertknowledgedocument_dao import Api137InsertknowledgedocumentDao
from app.dao.api138_insertdocumentversion.api138_insertdocumentversion_dao import Api138InsertdocumentversionDao
from app.dto.api137_insertknowledgedocument.api137_insertknowledgedocument_dto import Api137InsertknowledgedocumentDto
from app.dto.api138_insertdocumentversion.api138_insertdocumentversion_dto import Api138InsertdocumentversionDto
from app.dto.documentsaveapi.documentsaveapi_dto import DocumentsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DocumentsaveapiService :

	#	# 
	# ナレッジ文書新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentsaveapi(self,documentsaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		TITLE = documentsaveapi_dto.title#GeninusClientScript 1318
		CATEGORY = documentsaveapi_dto.category#GeninusClientScript 1318
		FORMAT = documentsaveapi_dto.format#GeninusClientScript 1318
		FILE = documentsaveapi_dto.file#GeninusClientScript 1318
		api137_insertknowledgedocument = Api137InsertknowledgedocumentDto.dict_to_json({}) #CommonFunction 110
		api138_insertdocumentversion = Api138InsertdocumentversionDto.dict_to_json({}) #CommonFunction 110
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書新規画面登録ボタン_DocumentSaveAPI_(API)
			
			#「項目処理」（共通関数:DocumentSaveAPI）,パラメータは（title,category,format,file）
			
			#以下の処理を行う。
			
			#関数「API137_InsertKnowledgeDocument」の「db_API137_InsertKnowledgeDocument」メソッドを行う,パラメータは「knowledge_document_id,document_code,title,category,format,active_version_number,prefecture_code」。
			
			# knowledge_document_id
			api137_insertknowledgedocument.knowledgedocumentid = KNOWLEDGE_DOCUMENT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# uploaded_date
			api137_insertknowledgedocument.uploadeddate = DOCUMENT_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# file_size_kb
			api137_insertknowledgedocument.filesizekb = TITLE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# status
			api137_insertknowledgedocument.status = CATEGORY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# file_path
			api137_insertknowledgedocument.filepath = FORMAT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			Api137InsertknowledgedocumentDao().api137_insertknowledgedocument(api137_insertknowledgedocument) #ResultGenerator 104
			#ResultGenerator 104
			#関数「API138_InsertDocumentVersion」の「db_API138_InsertDocumentVersion」メソッドを行う,パラメータは「knowledge_document_id,version_number,uploaded_by,file_size_kb,status,file_path」。
			
			# knowledge_document_id
			api138_insertdocumentversion.knowledgedocumentid = KNOWLEDGE_DOCUMENT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api138_insertdocumentversion.prefecturecode = VERSION_NUMBER #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# document_code
			api138_insertdocumentversion.documentcode = UPLOADED_BY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# title
			api138_insertdocumentversion.title = FILE_SIZE_KB #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# category
			api138_insertdocumentversion.category = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# format
			api138_insertdocumentversion.format = FILE_PATH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# created_by
			api138_insertdocumentversion.createdby = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# updated_by
			api138_insertdocumentversion.updatedby = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			Api138InsertdocumentversionDao().api138_insertdocumentversion(api138_insertdocumentversion) #ResultGenerator 104
			#ResultGenerator 104
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
