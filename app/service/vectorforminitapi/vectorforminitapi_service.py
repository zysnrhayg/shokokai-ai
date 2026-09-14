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
from app.dao.api177_vectorforminit.api177_vectorforminit_dao import Api177VectorforminitDao
from app.dto.api177_vectorforminit.api177_vectorforminit_dto import Api177VectorforminitDto
from app.dto.vectorforminitapi.vectorforminitapi_dto import VectorforminitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorforminitapiService :

	#	# 
	# ベクトルコレクション編集編集
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorforminitapi(self,vectorforminitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		ID = vectorforminitapi_dto.id#GeninusClientScript 1318
		api177_vectorforminit = Api177VectorforminitDto.dict_to_json({}) #CommonFunction 110
		api177_vectorforminitList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api177_vectorforminit_dto = None #ResultGenerator 119
		#ResultGenerator365
		VECTORCOLLECTIONID = ""
		COLLECTIONCODE = ""
		NAME = ""
		VECTORCOUNT = ""
		BASELINEVECTORCOUNT = ""
		STATUS = ""
		SYNCEDDATE = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトルコレクション編集編集_VectorFormInitAPI_(API)
			
			#「項目処理」（共通関数:VectorFormInitAPI）,パラメータは（id）
			
			#以下の処理を行う。
			
			#関数「API177_VectorFormInit」の「db_API177_VectorFormInit」メソッドを行う,パラメータは「vector_collection_id」,戻り値設定は「<vector_collection_id>=vector_collection_id,<collection_code>=collection_code,<name>=name,<vector_count>=vector_count,<baseline_vector_count>=baseline_vector_count,<status>=status,<synced_date>=synced_date」を設定する。
			
			# vector_collection_id
			api177_vectorforminit.vectorcollectionid = VECTOR_COLLECTION_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api177_vectorforminitList = Api177VectorforminitDao().api177_vectorforminit(api177_vectorforminit)
			api177_vectorforminitlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api177_vectorforminitList != None :
				api177_vectorforminitlistVar = api177_vectorforminitList.fetchall() if hasattr(api177_vectorforminitList, 'fetchall') else api177_vectorforminitList
			if api177_vectorforminitlistVar != None and len(api177_vectorforminitlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api177_vectorforminitlistVar))
			# --LINE114 retrieved first value
			if api177_vectorforminitlistVar != None and len(api177_vectorforminitlistVar) > 0 :
				rec = api177_vectorforminitlistVar[0]
				VECTORCOLLECTIONID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "vector_collection_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				COLLECTIONCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "collection_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
				VECTORCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "vector_count")) # ResultGenerator 385
				# ResultGenerator 385
				
				BASELINEVECTORCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "baseline_vector_count")) # ResultGenerator 385
				# ResultGenerator 385
				
				STATUS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status")) # ResultGenerator 385
				# ResultGenerator 385
				
				SYNCEDDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "synced_date")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
