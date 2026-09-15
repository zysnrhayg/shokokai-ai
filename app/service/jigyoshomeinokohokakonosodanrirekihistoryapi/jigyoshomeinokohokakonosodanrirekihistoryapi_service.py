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
from app.dao.api_jigyoshomeinokohokakonosodanrirekihistory.api_jigyoshomeinokohokakonosodanrirekihistory_dao import ApiJigyoshomeinokohokakonosodanrirekihistoryDao
from app.dto.api_jigyoshomeinokohokakonosodanrirekihistory.api_jigyoshomeinokohokakonosodanrirekihistory_dto import ApiJigyoshomeinokohokakonosodanrirekihistoryDto
from app.dto.jigyoshomeinokohokakonosodanrirekihistoryapi.jigyoshomeinokohokakonosodanrirekihistoryapi_dto import JigyoshomeinokohokakonosodanrirekihistoryapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class JigyoshomeinokohokakonosodanrirekihistoryapiService :

	#	# 
	# 事業所過去相談履歴
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def jigyoshomeinokohokakonosodanrirekihistoryapi(self,jigyoshomeinokohokakonosodanrirekihistoryapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		XX = jigyoshomeinokohokakonosodanrirekihistoryapi_dto.xx#GeninusClientScript 1318
		api_jigyoshomeinokohokakonosodanrirekihistory = ApiJigyoshomeinokohokakonosodanrirekihistoryDto.dict_to_json({}) #CommonFunction 110
		api_jigyoshomeinokohokakonosodanrirekihistoryList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api_jigyoshomeinokohokakonosodanrirekihistory_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#事業所過去相談履歴_JigyoshomeiNoKohoKakoNoSodanRirekiHistoryAPI_(API)
			
			#「項目処理」（共通関数:JigyoshomeiNoKohoKakoNoSodanRirekiHistoryAPI）,パラメータは（xx）
			
			#以下の処理を行う。
			
			#関数「API_JigyoshomeiNoKohoKakoNoSodanRirekiHistory」の「db_API_JigyoshomeiNoKohoKakoNoSodanRirekiHistory」メソッドを行う,パラメータは「trn_report.prefecture_code,trn_report.shokokai_cd,trn_report.business_name,LIMIT」,戻り値設定は「xx」。
			
			# trn_report.prefecture_code
			api_jigyoshomeinokohokakonosodanrirekihistory.trnreportprefecturecode = jigyoshomeinokohokakonosodanrirekihistoryapi_dto.trnreportprefecturecode #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# trn_report.shokokai_cd
			api_jigyoshomeinokohokakonosodanrirekihistory.trnreportshokokaicd = jigyoshomeinokohokakonosodanrirekihistoryapi_dto.trnreportshokokaicd #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# trn_report.business_name
			api_jigyoshomeinokohokakonosodanrirekihistory.trnreportbusinessname = jigyoshomeinokohokakonosodanrirekihistoryapi_dto.trnreportbusinessname #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# LIMIT
			api_jigyoshomeinokohokakonosodanrirekihistory.limit = jigyoshomeinokohokakonosodanrirekihistoryapi_dto.limit #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api_jigyoshomeinokohokakonosodanrirekihistoryList = ApiJigyoshomeinokohokakonosodanrirekihistoryDao().api_jigyoshomeinokohokakonosodanrirekihistory(api_jigyoshomeinokohokakonosodanrirekihistory)
			api_jigyoshomeinokohokakonosodanrirekihistorylistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_jigyoshomeinokohokakonosodanrirekihistoryList != None :
				api_jigyoshomeinokohokakonosodanrirekihistorylistVar = api_jigyoshomeinokohokakonosodanrirekihistoryList.fetchall() if hasattr(api_jigyoshomeinokohokakonosodanrirekihistoryList, 'fetchall') else api_jigyoshomeinokohokakonosodanrirekihistoryList
			if api_jigyoshomeinokohokakonosodanrirekihistorylistVar != None and len(api_jigyoshomeinokohokakonosodanrirekihistorylistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_jigyoshomeinokohokakonosodanrirekihistorylistVar))
			# --LINE114 retrieved first value
			if api_jigyoshomeinokohokakonosodanrirekihistorylistVar != None and len(api_jigyoshomeinokohokakonosodanrirekihistorylistVar) > 0 :
				rec = api_jigyoshomeinokohokakonosodanrirekihistorylistVar[0]
			#関数「API_JigyoshomeiNoKohoKakoNoSodanRirekiHistory」の「db_API_JigyoshomeiNoKohoKakoNoSodanRirekiHistory」取得結果をJSON形式でGrid「rows」に設定し,20行で改ページする。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api_jigyoshomeinokohokakonosodanrirekihistorylistVar != None and len(api_jigyoshomeinokohokakonosodanrirekihistorylistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_jigyoshomeinokohokakonosodanrirekihistorylistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_jigyoshomeinokohokakonosodanrirekihistorylistVar[i]
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
		
			
	
	
