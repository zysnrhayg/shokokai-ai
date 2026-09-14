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
		#ResultGenerator365
		VECTORCOLLECTIONID = ""
		COLLECTIONCODE = ""
		NAME = ""
		VECTORCOUNT = ""
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
			if api_bekutorukorekushonichiranlistVar != None and len(api_bekutorukorekushonichiranlistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_bekutorukorekushonichiranlistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_bekutorukorekushonichiranlistVar[i]
					selMap ={} #GeniusGrid681
					#GeniusGrid681
					mapList.insert(len(mapList),selMap)
			result = json.dumps(mapList, ensure_ascii=False)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			#関数「API_RAGsettei」の「db_API_RAGsettei」メソッドを行う,パラメータは「」,戻り値設定は「<vector_collection_id>=vector_collection_id,<collection_code>=collection_code,<name>=name,<vector_count>=vector_count」を設定する。
			
			#ReulstGenerator 87
			api_ragsetteiList = ApiRagsetteiDao().api_ragsettei(api_ragsettei)
			api_ragsetteilistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_ragsetteiList != None :
				api_ragsetteilistVar = api_ragsetteiList.fetchall() if hasattr(api_ragsetteiList, 'fetchall') else api_ragsetteiList
			if api_ragsetteilistVar != None and len(api_ragsetteilistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_ragsetteilistVar))
			# --LINE114 retrieved first value
			if api_ragsetteilistVar != None and len(api_ragsetteilistVar) > 0 :
				rec = api_ragsetteilistVar[0]
				VECTORCOLLECTIONID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "vector_collection_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				COLLECTIONCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "collection_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
				VECTORCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "vector_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
