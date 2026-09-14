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
from app.dao.api153_resyncvectorcollections.api153_resyncvectorcollections_dao import Api153ResyncvectorcollectionsDao
from app.dto.api153_resyncvectorcollections.api153_resyncvectorcollections_dto import Api153ResyncvectorcollectionsDto
from app.dto.vectorsresyncapi.vectorsresyncapi_dto import VectorsresyncapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorsresyncapiService :

	#	# 
	# ベクトル一覧画面再同期ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorsresyncapi(self,vectorsresyncapi_dto,jsonObj) :
			
		api153_resyncvectorcollections = Api153ResyncvectorcollectionsDto.dict_to_json({}) #CommonFunction 110
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトル一覧画面再同期ボタン_VectorsResyncAPI_(API)
			
			#「項目処理」（共通関数:VectorsResyncAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API153_ResyncVectorCollections」の「db_API153_ResyncVectorCollections」メソッドを行う,パラメータは「vector_collection_id,vector_count」。
			
			# vector_collection_id
			api153_resyncvectorcollections.vectorcollectionid = VECTOR_COLLECTION_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# vector_count
			api153_resyncvectorcollections.vectorcount = VECTOR_COUNT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			Api153ResyncvectorcollectionsDao().api153_resyncvectorcollections(api153_resyncvectorcollections) #ResultGenerator 104
			#ResultGenerator 104
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
