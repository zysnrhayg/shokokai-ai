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
from app.dao.api_genponbunshoichiran.api_genponbunshoichiran_dao import ApiGenponbunshoichiranDao
from app.dto.api_genponbunshoichiran.api_genponbunshoichiran_dto import ApiGenponbunshoichiranDto
from app.dto.knowledgeinitapi.knowledgeinitapi_dto import KnowledgeinitapiDto
from app.accounts.services import resolve_account_role
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class KnowledgeinitapiService :

	#	# 
	# ナレッジ文書一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def knowledgeinitapi(self,knowledgeinitapi_dto,jsonObj) :
			
		api_genponbunshoichiran = ApiGenponbunshoichiranDto.dict_to_json({}) #CommonFunction 110
		# 顧客設計：県連ロールのみ prefecture_code（全国共有 IS NULL または自県）で絞込。全国ロールは絞込なし。
		if resolve_account_role() == "pref":
			api_genponbunshoichiran.prefecturecode = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
		else:
			api_genponbunshoichiran.prefecturecode = ""
		api_genponbunshoichiranList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api_genponbunshoichiran_dto = None #ResultGenerator 119
		#ResultGenerator365
		KNOWLEDGEDOCUMENTID = ""
		DOCUMENTCODE = ""
		TITLE = ""
		CATEGORY = ""
		FORMAT = ""
		ACTIVEVERSIONNUMBER = ""
		UPLOADEDDATE = ""
		FILESIZEKB = ""
		STATUS = ""
		ENTRYCOUNT = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書一覧画面初期表示_KnowledgeInitAPI_(API)
			
			#「項目処理」（共通関数:KnowledgeInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API_GenponBunshoIchiran」の「db_API_GenponBunshoIchiran」メソッドを行う,パラメータは「prefecture_code」,戻り値設定は「<knowledge_document_id>=knowledge_document_id,<document_code>=document_code,<title>=title,<category>=category,<format>=format,<active_version_number>=active_version_number,<uploaded_date>=uploaded_date,<file_size_kb>=file_size_kb,<status>=status,<entry_count>=entry_count」を設定する。
			
			#ReulstGenerator 87
			api_genponbunshoichiranList = ApiGenponbunshoichiranDao().api_genponbunshoichiran(api_genponbunshoichiran)
			api_genponbunshoichiranlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_genponbunshoichiranList != None :
				api_genponbunshoichiranlistVar = api_genponbunshoichiranList.fetchall() if hasattr(api_genponbunshoichiranList, 'fetchall') else api_genponbunshoichiranList
			if api_genponbunshoichiranlistVar != None and len(api_genponbunshoichiranlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_genponbunshoichiranlistVar))
			# --LINE114 retrieved first value
			if api_genponbunshoichiranlistVar != None and len(api_genponbunshoichiranlistVar) > 0 :
				rec = api_genponbunshoichiranlistVar[0]
				KNOWLEDGEDOCUMENTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				DOCUMENTCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "document_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				TITLE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title")) # ResultGenerator 385
				# ResultGenerator 385
				
				CATEGORY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "category")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMAT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "format")) # ResultGenerator 385
				# ResultGenerator 385
				
				ACTIVEVERSIONNUMBER = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "active_version_number")) # ResultGenerator 385
				# ResultGenerator 385
				
				UPLOADEDDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "uploaded_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				FILESIZEKB = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "file_size_kb")) # ResultGenerator 385
				# ResultGenerator 385
				
				STATUS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status")) # ResultGenerator 385
				# ResultGenerator 385
				
				ENTRYCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "entry_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API_GenponBunshoIchiran」の「db_API_GenponBunshoIchiran」取得結果をJSON形式でGrid「documents」に設定し,20行で改ページする。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api_genponbunshoichiranlistVar != None and len(api_genponbunshoichiranlistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_genponbunshoichiranlistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_genponbunshoichiranlistVar[i]
					selMap ={} #GeniusGrid681
					#GeniusGrid681
					# API_GenponBunshoIchiranの取得結果を、Grid「documents」の1行分のデータとして設定する。
					selMap["knowledge_document_id"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "knowledge_document_id"))
					selMap["document_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "document_code"))
					selMap["title"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "title"))
					selMap["category"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "category"))
					selMap["format"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "format"))
					selMap["active_version_number"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "active_version_number"))
					selMap["prefecture_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "prefecture_code"))
					selMap["prefecture_name"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "prefecture_name"))
					selMap["uploaded_date"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "uploaded_date"))
					selMap["file_size_kb"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "file_size_kb"))
					selMap["status"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "status"))
					selMap["file_path"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "file_path"))
					selMap["linked_count"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "linked_count"))
					mapList.insert(len(mapList),selMap)
			result = json.dumps(mapList, default=str, ensure_ascii=False)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
