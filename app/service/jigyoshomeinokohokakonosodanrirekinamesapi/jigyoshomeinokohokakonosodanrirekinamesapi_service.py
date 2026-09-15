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
from app.dao.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_dao import ApiJigyoshomeinokohokakonosodanrirekinamesDao
from app.dto.api_jigyoshomeinokohokakonosodanrirekinames.api_jigyoshomeinokohokakonosodanrirekinames_dto import ApiJigyoshomeinokohokakonosodanrirekinamesDto
from app.dto.jigyoshomeinokohokakonosodanrirekinamesapi.jigyoshomeinokohokakonosodanrirekinamesapi_dto import JigyoshomeinokohokakonosodanrirekinamesapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class JigyoshomeinokohokakonosodanrirekinamesapiService :

	#	# 
	# 事業所名サジェスト
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def jigyoshomeinokohokakonosodanrirekinamesapi(self,jigyoshomeinokohokakonosodanrirekinamesapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		XX = jigyoshomeinokohokakonosodanrirekinamesapi_dto.xx#GeninusClientScript 1318
		api_jigyoshomeinokohokakonosodanrirekinames = ApiJigyoshomeinokohokakonosodanrirekinamesDto.dict_to_json({}) #CommonFunction 110
		api_jigyoshomeinokohokakonosodanrirekinamesList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api_jigyoshomeinokohokakonosodanrirekinames_dto = None #ResultGenerator 119
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#事業所名サジェスト_JigyoshomeiNoKohoKakoNoSodanRirekiNamesAPI_(API)
			
			#「項目処理」（共通関数:JigyoshomeiNoKohoKakoNoSodanRirekiNamesAPI）,パラメータは（xx）
			
			#以下の処理を行う。
			
			#関数「API_JigyoshomeiNoKohoKakoNoSodanRirekiNames」の「db_API_JigyoshomeiNoKohoKakoNoSodanRirekiNames」メソッドを行う,パラメータは「prefecture_code,shokokai_cd,LIMIT」,戻り値設定は「xx」。
			
			# prefecture_code
			api_jigyoshomeinokohokakonosodanrirekinames.prefecturecode = jigyoshomeinokohokakonosodanrirekinamesapi_dto.prefecturecode #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api_jigyoshomeinokohokakonosodanrirekinames.shokokaicd = jigyoshomeinokohokakonosodanrirekinamesapi_dto.shokokaicd #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# LIMIT
			api_jigyoshomeinokohokakonosodanrirekinames.limit = jigyoshomeinokohokakonosodanrirekinamesapi_dto.limit #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api_jigyoshomeinokohokakonosodanrirekinamesList = ApiJigyoshomeinokohokakonosodanrirekinamesDao().api_jigyoshomeinokohokakonosodanrirekinames(api_jigyoshomeinokohokakonosodanrirekinames)
			api_jigyoshomeinokohokakonosodanrirekinameslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_jigyoshomeinokohokakonosodanrirekinamesList != None :
				api_jigyoshomeinokohokakonosodanrirekinameslistVar = api_jigyoshomeinokohokakonosodanrirekinamesList.fetchall() if hasattr(api_jigyoshomeinokohokakonosodanrirekinamesList, 'fetchall') else api_jigyoshomeinokohokakonosodanrirekinamesList
			if api_jigyoshomeinokohokakonosodanrirekinameslistVar != None and len(api_jigyoshomeinokohokakonosodanrirekinameslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_jigyoshomeinokohokakonosodanrirekinameslistVar))
			# --LINE114 retrieved first value
			if api_jigyoshomeinokohokakonosodanrirekinameslistVar != None and len(api_jigyoshomeinokohokakonosodanrirekinameslistVar) > 0 :
				rec = api_jigyoshomeinokohokakonosodanrirekinameslistVar[0]
			#関数「API_JigyoshomeiNoKohoKakoNoSodanRirekiNames」の「db_API_JigyoshomeiNoKohoKakoNoSodanRirekiNames」取得結果をJSON形式でGrid「rows」に設定し,20行で改ページする。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api_jigyoshomeinokohokakonosodanrirekinameslistVar != None and len(api_jigyoshomeinokohokakonosodanrirekinameslistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api_jigyoshomeinokohokakonosodanrirekinameslistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api_jigyoshomeinokohokakonosodanrirekinameslistVar[i]
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
		
			
	
	
