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
from app.dao.api155_verify2fainit.api155_verify2fainit_dao import Api155Verify2fainitDao
from app.dto.api155_verify2fainit.api155_verify2fainit_dto import Api155Verify2fainitDto
from app.dto.verify2fainitapi.verify2fainitapi_dto import Verify2fainitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class Verify2fainitapiService :

	#	# 
	# 二段階認証画面画面を開く
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def verify2fainitapi(self,verify2fainitapi_dto,jsonObj) :
			
		api155_verify2fainit = Api155Verify2fainitDto.dict_to_json({}) #CommonFunction 110
		api155_verify2fainitList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api155_verify2fainit_dto = None #ResultGenerator 119
		#ResultGenerator365
		XXX = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#二段階認証画面画面を開く_Verify2faInitAPI_(API)
			
			#「項目処理」（共通関数:Verify2faInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API155_Verify2faInit」の「db_API155_Verify2faInit」取得結果をJSON形式で「init_data」に設定。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			#関数「API155_Verify2faInit」の「db_API155_Verify3faInit」メソッドを行う,パラメータは「」,戻り値設定は「<xxx>=result」を設定する。
			
			#ReulstGenerator 87
			api155_verify2fainitList = Api155Verify2fainitDao().api155_verify2fainit(api155_verify2fainit)
			api155_verify2fainitlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api155_verify2fainitList != None :
				api155_verify2fainitlistVar = api155_verify2fainitList.fetchall() if hasattr(api155_verify2fainitList, 'fetchall') else api155_verify2fainitList
			if api155_verify2fainitlistVar != None and len(api155_verify2fainitlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api155_verify2fainitlistVar))
			# --LINE114 retrieved first value
			if api155_verify2fainitlistVar != None and len(api155_verify2fainitlistVar) > 0 :
				rec = api155_verify2fainitlistVar[0]
				XXX = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "result")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
