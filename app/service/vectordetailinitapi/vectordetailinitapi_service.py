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
from app.dao.api149_getvectorcollectiondetail.api149_getvectorcollectiondetail_dao import Api149GetvectorcollectiondetailDao
from app.dto.api149_getvectorcollectiondetail.api149_getvectorcollectiondetail_dto import Api149GetvectorcollectiondetailDto
from app.dto.vectordetailinitapi.vectordetailinitapi_dto import VectordetailinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectordetailinitapiService :

	#	# 
	# ベクトル詳細画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectordetailinitapi(self,vectordetailinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		VECTOR_COLLECTION_ID = vectordetailinitapi_dto.vectorcollectionid#GeninusClientScript 1318
		api149_getvectorcollectiondetail = Api149GetvectorcollectiondetailDto.dict_to_json({}) #CommonFunction 110
		api149_getvectorcollectiondetailList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api149_getvectorcollectiondetail_dto = None #ResultGenerator 119
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
			#ベクトル詳細画面初期表示_VectorDetailInitAPI_(API)
			
			#「項目処理」（共通関数:VectorDetailInitAPI）,パラメータは（vector_collection_id）
			
			#以下の処理を行う。
			
			#関数「API149_GetVectorCollectionDetail」の「db_API149_GetVectorCollectionDetail」メソッドを行う,パラメータは「vector_collection_id」,戻り値設定は「<vector_collection_id>=vector_collection_id,<collection_code>=collection_code,<name>=name,<vector_count>=vector_count,<baseline_vector_count>=baseline_vector_count,<status>=status,<synced_date>=synced_date」を設定する。
			
			# vector_collection_id
			api149_getvectorcollectiondetail.vectorcollectionid = VECTOR_COLLECTION_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api149_getvectorcollectiondetailList = Api149GetvectorcollectiondetailDao().api149_getvectorcollectiondetail(api149_getvectorcollectiondetail)
			api149_getvectorcollectiondetaillistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api149_getvectorcollectiondetailList != None :
				api149_getvectorcollectiondetaillistVar = api149_getvectorcollectiondetailList.fetchall() if hasattr(api149_getvectorcollectiondetailList, 'fetchall') else api149_getvectorcollectiondetailList
			if api149_getvectorcollectiondetaillistVar != None and len(api149_getvectorcollectiondetaillistVar) > 0 :
				SHUTOKUKENSUU = str(len(api149_getvectorcollectiondetaillistVar))
			# --LINE114 retrieved first value
			if api149_getvectorcollectiondetaillistVar != None and len(api149_getvectorcollectiondetaillistVar) > 0 :
				rec = api149_getvectorcollectiondetaillistVar[0]
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
		
			
	
	
