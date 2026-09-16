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
from app.dao.api_bekutorukorekushonichiran.api_bekutorukorekushonichiran_dao import ApiBekutorukorekushonichiranDao
from app.dao.api_ragsettei.api_ragsettei_dao import ApiRagsetteiDao
from app.dto.api_bekutorukorekushonichiran.api_bekutorukorekushonichiran_dto import ApiBekutorukorekushonichiranDto
from app.dto.api_ragsettei.api_ragsettei_dto import ApiRagsetteiDto
from app.dto.vectorsinitapi.vectorsinitapi_dto import VectorsinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorsinitapiService :

	#	# 
	# ベクトル一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorsinitapi(self,vectorsinitapi_dto,jsonObj) :
			
		api_bekutorukorekushonichiran = ApiBekutorukorekushonichiranDto.dict_to_json({}) #CommonFunction 110
		api_bekutorukorekushonichiranList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api_bekutorukorekushonichiran_dto = None #ResultGenerator 119
		api_ragsettei = ApiRagsetteiDto.dict_to_json({}) #CommonFunction 110
		api_ragsetteiList = None #ResultGenerator 72
		#_dto api_ragsettei_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトル一覧画面初期表示_VectorsInitAPI_(API)

			#「項目処理」（共通関数:VectorsInitAPI）,パラメータは（）

			#以下の処理を行う。

			#関数「API_BekutorukorekushonIchiran」の「db_API_BekutorukorekushonIchiran」メソッドを行う,パラメータは「」,戻り値設定は「」を設定する。

			#ReulstGenerator 87
			api_bekutorukorekushonichiranList = ApiBekutorukorekushonichiranDao().api_bekutorukorekushonichiran(api_bekutorukorekushonichiran)
			api_bekutorukorekushonichiranlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_bekutorukorekushonichiranList != None :
				api_bekutorukorekushonichiranlistVar = api_bekutorukorekushonichiranList.fetchall() if hasattr(api_bekutorukorekushonichiranList, 'fetchall') else api_bekutorukorekushonichiranList
			if api_bekutorukorekushonichiranlistVar != None and len(api_bekutorukorekushonichiranlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_bekutorukorekushonichiranlistVar))
			# --LINE114 retrieved first value
			if api_bekutorukorekushonichiranlistVar != None and len(api_bekutorukorekushonichiranlistVar) > 0 :
				rec = api_bekutorukorekushonichiranlistVar[0]
			#関数「API_BekutorukorekushonIchiran」の「db_API_BekutorukorekushonIchiran」取得結果をJSON形式でGrid「collections」に設定し,20行で改ページする。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			# ベクトル一覧データをGrid「dragB」に設定する（フロントエンド表示用）
			if api_bekutorukorekushonichiranlistVar != None and len(api_bekutorukorekushonichiranlistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_bekutorukorekushonichiranlistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_bekutorukorekushonichiranlistVar[i]
					# ステータスに応じたバッジクラスを設定する
					status = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "status"))
					status_badge_class = "badge-status-ok" if status == "同期済み" else "badge-status-pending"
					selMap = {
						"vector_collection_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "vector_collection_id")),
						"collection_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "collection_code")),
						"name": utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "name")),
						"vector_count": utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "vector_count")),
						"baseline_vector_count": utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "baseline_vector_count")),
						"synced_date": utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "synced_date")),
						"status": status,
						"status_badge_class": status_badge_class
					} #GeniusGrid681
					#GeniusGrid681
					mapList.insert(len(mapList),selMap)
			# ベクトル一覧データをJSON形式でフロントエンドに返却する
			result = json.dumps(mapList, ensure_ascii=False, default=str)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			#関数「API_RAGsettei」の「db_API_RAGsettei」メソッドを行う,パラメータは「」,戻り値設定は「」を設定する。

			#ReulstGenerator 87
			api_ragsetteiList = ApiRagsetteiDao().api_ragsettei(api_ragsettei)
			api_ragsetteilistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_ragsetteiList != None :
				api_ragsetteilistVar = api_ragsetteiList.fetchall() if hasattr(api_ragsetteiList, 'fetchall') else api_ragsetteiList
			if api_ragsetteilistVar != None and len(api_ragsetteilistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_ragsetteilistVar))
			# --LINE114 retrieved first value
			# RAG設定をJSON形式でフロントエンドに返却する
			ragInfo = {}
			if api_ragsetteilistVar != None and len(api_ragsetteilistVar) > 0 :
				rec = api_ragsetteilistVar[0]
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
		
			
	
	
