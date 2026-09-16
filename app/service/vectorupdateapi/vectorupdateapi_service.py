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
from app.dao.api151_updatevectorcollection.api151_updatevectorcollection_dao import Api151UpdatevectorcollectionDao
from app.dto.api151_updatevectorcollection.api151_updatevectorcollection_dto import Api151UpdatevectorcollectionDto
from app.dto.vectorupdateapi.vectorupdateapi_dto import VectorupdateapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorupdateapiService :

	#	# 
	# ベクトル編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorupdateapi(self,vectorupdateapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		VECTOR_COLLECTION_ID = vectorupdateapi_dto.vectorcollectionid#GeninusClientScript 1318
		NAME = vectorupdateapi_dto.name#GeninusClientScript 1318
		VECTOR_COUNT = vectorupdateapi_dto.vectorcount#GeninusClientScript 1318
		STATUS = vectorupdateapi_dto.status#GeninusClientScript 1318
		api151_updatevectorcollection = Api151UpdatevectorcollectionDto.dict_to_json({}) #CommonFunction 110
		KOUSHINKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトル編集画面登録ボタン_VectorUpdateAPI_(API)

			#「項目処理」（共通関数:VectorUpdateAPI）,パラメータは（vector_collection_id,name,vector_count,status）

			#以下の処理を行う。

			#関数「API151_UpdateVectorCollection」の「db_API151_UpdateVectorCollection」メソッドを行う,パラメータは「name,vector_count,status,vector_collection_id」。

			# name
			api151_updatevectorcollection.name = NAME #ArgumentGenerator 274
			#ArgumentGenerator 274

			# vector_count
			api151_updatevectorcollection.vectorcount = VECTOR_COUNT #ArgumentGenerator 274
			#ArgumentGenerator 274

			# status
			api151_updatevectorcollection.status = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274

			# vector_collection_id
			api151_updatevectorcollection.vectorcollectionid = VECTOR_COLLECTION_ID #ArgumentGenerator 274
			#ArgumentGenerator 274

			updateResult = Api151UpdatevectorcollectionDao().api151_updatevectorcollection(api151_updatevectorcollection) #ResultGenerator 104
			#ResultGenerator 104
			# 更新件数を取得する
			KOUSHINKENSUU = str(len(updateResult)) if updateResult != None else "0"
			#<更新件数>が"1"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if KOUSHINKENSUU.replace(" ", "") == "1" : #GeniusContion 823
				#GeniusContion 823
				#「更新しました」メッセージを表示する。
				jsonObj.setScript(utils.json_constant.JSONID_MSG, "更新しました")
				#処理終了。
				pass
				#GeniusClientScript 1207
			else:
				# 更新失敗時のメッセージを表示する
				jsonObj.setScript(utils.json_constant.JSONID_MSG, "更新に失敗しました")
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
