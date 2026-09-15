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
from app.dao.api135_getknowledgedocumentdetail.api135_getknowledgedocumentdetail_dao import Api135GetknowledgedocumentdetailDao
from app.dto.api135_getknowledgedocumentdetail.api135_getknowledgedocumentdetail_dto import Api135GetknowledgedocumentdetailDto
from app.dto.documentdetailinitapi.documentdetailinitapi_dto import DocumentdetailinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DocumentdetailinitapiService :

	#	#
	# ナレッジ文書詳細画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentdetailinitapi(self,documentdetailinitapi_dto,jsonObj) :

		#GeniusClientScript 1315
		KNOWLEDGE_DOCUMENT_ID = documentdetailinitapi_dto.knowledgedocumentid#GeninusClientScript 1318
		api135_getknowledgedocumentdetail = Api135GetknowledgedocumentdetailDto.dict_to_json({}) #CommonFunction 110
		api135_getknowledgedocumentdetailList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api135_getknowledgedocumentdetail_dto = None #ResultGenerator 119
		#ResultGenerator365
		KNOWLEDGEDOCUMENTID = ""
		DOCUMENTCODE = ""
		TITLE = ""
		CATEGORY = ""
		FORMAT = ""
		ACTIVEVERSIONNUMBER = ""
		PREFECTURECODE = ""
		PREFECTURENAME = ""
		FILESIZEKB = ""
		UPLOADEDDATE = ""
		STATUS = ""
		FILEPATH = ""
		LINKEDCOUNT = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書詳細画面初期表示_DocumentDetailInitAPI_(API)

			#「項目処理」（共通関数:DocumentDetailInitAPI）,パラメータは（knowledge_document_id）

			#以下の処理を行う。

			#関数「API135_GetKnowledgeDocumentDetail」の「db_API135_GetKnowledgeDocumentDetail」メソッドを行う,パラメータは「knowledge_document_id」,戻り値設定は「<knowledge_document_id>=knowledge_document_id,<document_code>=document_code,<title>=title,<category>=category,<format>=format,<active_version_number>=active_version_number,<prefecture_code>=prefecture_code,<prefecture_name>=prefecture_name」を設定する。

			# knowledge_document_id
			api135_getknowledgedocumentdetail.knowledgedocumentid = KNOWLEDGE_DOCUMENT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274

			#ReulstGenerator 87
			api135_getknowledgedocumentdetailList = Api135GetknowledgedocumentdetailDao().api135_getknowledgedocumentdetail(api135_getknowledgedocumentdetail)
			api135_getknowledgedocumentdetaillistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api135_getknowledgedocumentdetailList != None :
				api135_getknowledgedocumentdetaillistVar = api135_getknowledgedocumentdetailList.fetchall() if hasattr(api135_getknowledgedocumentdetailList, 'fetchall') else api135_getknowledgedocumentdetailList
			if api135_getknowledgedocumentdetaillistVar != None and len(api135_getknowledgedocumentdetaillistVar) > 0 :
				SHUTOKUKENSUU = str(len(api135_getknowledgedocumentdetaillistVar))
			# --LINE114 retrieved first value
			if api135_getknowledgedocumentdetaillistVar != None and len(api135_getknowledgedocumentdetaillistVar) > 0 :
				rec = api135_getknowledgedocumentdetaillistVar[0]
				KNOWLEDGEDOCUMENTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id")) # ResultGenerator 385
				DOCUMENTCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "document_code")) # ResultGenerator 385
				TITLE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title")) # ResultGenerator 385
				CATEGORY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "category")) # ResultGenerator 385
				FORMAT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "format")) # ResultGenerator 385
				ACTIVEVERSIONNUMBER = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "active_version_number")) # ResultGenerator 385
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				PREFECTURENAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_name")) # ResultGenerator 385
				FILESIZEKB = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "file_size_kb")) # ResultGenerator 385
				UPLOADEDDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "uploaded_date")) # ResultGenerator 385
				STATUS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status")) # ResultGenerator 385
				FILEPATH = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "file_path")) # ResultGenerator 385
				LINKEDCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "linked_count")) # ResultGenerator 385

			# 取得した文書詳細データをJSONとしてフロントエンドに返却する
			detailMap = {
				"knowledge_document_id": KNOWLEDGEDOCUMENTID,
				"document_code": DOCUMENTCODE,
				"title": TITLE,
				"category": CATEGORY,
				"format": FORMAT,
				"active_version_number": ACTIVEVERSIONNUMBER,
				"prefecture_code": PREFECTURECODE,
				"prefecture_name": PREFECTURENAME,
				"file_size_kb": FILESIZEKB,
				"uploaded_date": UPLOADEDDATE,
				"status": STATUS,
				"file_path": FILEPATH,
				"linked_count": LINKEDCOUNT
			}
			jsonObj.setHtml("documentDetail", json.dumps(detailMap, default=str, ensure_ascii=False))

			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
