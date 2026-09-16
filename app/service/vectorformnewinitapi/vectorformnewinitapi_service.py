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
from app.dao.api178_vectorformnewinit.api178_vectorformnewinit_dao import Api178VectorformnewinitDao
from app.dto.vectorformnewinitapi.vectorformnewinitapi_dto import VectorformnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorformnewinitapiService :

	#	#
	# ベクトルコレクション新規＋ コレクションを登録
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorformnewinitapi(self,vectorformnewinitapi_dto,jsonObj) :

		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトルコレクション新規＋ コレクションを登録_VectorFormNewInitAPI_(API)

			#「項目処理」（共通関数:VectorFormNewInitAPI）,パラメータは（）

			#以下の処理を行う。

			# RAG設定を取得する（cfg_rag_settingから最新1件）
			ragList = Api178VectorformnewinitDao().api178_vectorformnewinit(None)
			ragInfo = {}
			if ragList != None and len(ragList) > 0 :
				rec = ragList[0]
				ragInfo = {
					"rag_setting_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "rag_setting_id")),
					"embedding_model": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "embedding_model")),
					"vector_db": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "vector_db")),
					"chunk_size": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "chunk_size")),
					"chunk_overlap": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "chunk_overlap")),
					"last_synced_at": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "last_synced_at"))
				}
			# RAG設定をJSON形式でフロントエンドに返却する
			jsonObj.setHtml("ragSetting", json.dumps(ragInfo, ensure_ascii=False, default=str))
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
		
			
	
	
