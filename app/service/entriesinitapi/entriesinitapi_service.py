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
from app.dao.api_chishikidetaichiran.api_chishikidetaichiran_dao import ApiChishikidetaichiranDao
from app.dto.api_chishikidetaichiran.api_chishikidetaichiran_dto import ApiChishikidetaichiranDto
from app.dto.entriesinitapi.entriesinitapi_dto import EntriesinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntriesinitapiService :

	#	# 
	# 知識データ一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entriesinitapi(self,entriesinitapi_dto,jsonObj) :
			
		api_chishikidetaichiran = ApiChishikidetaichiranDto.dict_to_json({}) #CommonFunction 110
		api_chishikidetaichiranList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api_chishikidetaichiran_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ一覧画面初期表示_EntriesInitAPI_(API)
			
			#「項目処理」（共通関数:EntriesInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API_ChishikiDetaIchiran」の「db_API_ChishikiDetaIchiran」メソッドを行う,パラメータは「」,戻り値設定は「」を設定する。
			
			#ReulstGenerator 87
			api_chishikidetaichiranList = ApiChishikidetaichiranDao().api_chishikidetaichiran(api_chishikidetaichiran)
			api_chishikidetaichiranlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_chishikidetaichiranList != None :
				api_chishikidetaichiranlistVar = api_chishikidetaichiranList.fetchall() if hasattr(api_chishikidetaichiranList, 'fetchall') else api_chishikidetaichiranList
			if api_chishikidetaichiranlistVar != None and len(api_chishikidetaichiranlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_chishikidetaichiranlistVar))
			# --LINE114 retrieved first value
			if api_chishikidetaichiranlistVar != None and len(api_chishikidetaichiranlistVar) > 0 :
				rec = api_chishikidetaichiranlistVar[0]
			#関数「API_ChishikiDetaIchiran」の「db_API_ChishikiDetaIchiran」取得結果をJSON形式でGrid「entries」に設定し,20行で改ページする。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api_chishikidetaichiranlistVar != None and len(api_chishikidetaichiranlistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_chishikidetaichiranlistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_chishikidetaichiranlistVar[i]
					selMap ={} #GeniusGrid681
					#GeniusGrid681
					mapList.insert(len(mapList),selMap)
			result = json.dumps(mapList, ensure_ascii=False)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
