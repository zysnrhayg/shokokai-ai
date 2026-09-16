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
from app.dao.api150_insertvectorcollection.api150_insertvectorcollection_dao import Api150InsertvectorcollectionDao
from app.dto.api150_insertvectorcollection.api150_insertvectorcollection_dto import Api150InsertvectorcollectionDto
from app.dto.vectorsaveapi.vectorsaveapi_dto import VectorsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorsaveapiService :

	#	# 
	# ベクトル新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorsaveapi(self,vectorsaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		NAME = vectorsaveapi_dto.name#GeninusClientScript 1318
		api150_insertvectorcollection = Api150InsertvectorcollectionDto.dict_to_json({}) #CommonFunction 110
		TOUROKUKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトル新規画面登録ボタン_VectorSaveAPI_(API)

			#「項目処理」（共通関数:VectorSaveAPI）,パラメータは（name, vector_count, status）

			#以下の処理を行う。

			# フロントエンドから送信されたベクトル数とステータスを取得する
			# 未指定の場合はデフォルト値（vector_count=0, status=未同期）を使用する
			VECTOR_COUNT = vectorsaveapi_dto.vectorcount if vectorsaveapi_dto.vectorcount else 0
			BASELINE_VECTOR_COUNT = VECTOR_COUNT
			STATUS = vectorsaveapi_dto.status if vectorsaveapi_dto.status else "未同期"

			#関数「API150_InsertVectorCollection」の「db_API150_InsertVectorCollection」メソッドを行う,パラメータは「name,vector_count,baseline_vector_count,status」。

			# name
			api150_insertvectorcollection.name = NAME #ArgumentGenerator 274
			#ArgumentGenerator 274

			# vector_count
			api150_insertvectorcollection.vectorcount = VECTOR_COUNT #ArgumentGenerator 274
			#ArgumentGenerator 274

			# baseline_vector_count
			api150_insertvectorcollection.baselinevectorcount = BASELINE_VECTOR_COUNT #ArgumentGenerator 274
			#ArgumentGenerator 274

			# status
			api150_insertvectorcollection.status = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274

			insertResult = Api150InsertvectorcollectionDao().api150_insertvectorcollection(api150_insertvectorcollection) #ResultGenerator 104
			#ResultGenerator 104
			# 登録件数を取得する
			TOUROKUKENSUU = str(len(insertResult)) if insertResult != None else "0"
			#<登録件数>が"1"の場合,以下の処理を行う。
			#GeniusClientScript 983
			if TOUROKUKENSUU.replace(" ", "") == "1" : #GeniusContion 823
				#GeniusContion 823
				#「登録しました」メッセージを表示する。
				jsonObj.setScript(utils.json_constant.JSONID_MSG, "登録しました")
				#処理終了。
				pass
				#GeniusClientScript 1207
			else:
				# 登録失敗時のメッセージを表示する
				jsonObj.setScript(utils.json_constant.JSONID_MSG, "登録に失敗しました")
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
