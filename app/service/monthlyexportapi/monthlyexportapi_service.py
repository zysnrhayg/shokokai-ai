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
from app.dao.api169_monthlyexport.api169_monthlyexport_dao import Api169MonthlyexportDao
from app.dto.api169_monthlyexport.api169_monthlyexport_dto import Api169MonthlyexportDto
from app.dto.monthlyexportapi.monthlyexportapi_dto import MonthlyexportapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class MonthlyexportapiService :

	#	# 
	# 月次報告月次帳票出力
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def monthlyexportapi(self,monthlyexportapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		FORM_CODE = monthlyexportapi_dto.formcode#GeninusClientScript 1318
		FISCAL_YEAR_CODE = monthlyexportapi_dto.fiscalyearcode#GeninusClientScript 1318
		api169_monthlyexport = Api169MonthlyexportDto.dict_to_json({}) #CommonFunction 110
		api169_monthlyexportList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api169_monthlyexport_dto = None #ResultGenerator 119
		#ResultGenerator365
		RESULT = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#月次報告月次帳票出力_MonthlyExportAPI_(API)
			
			#「項目処理」（共通関数:MonthlyExportAPI）,パラメータは（form_code,fiscal_year_code）
			
			#以下の処理を行う。
			
			#関数「API169_MonthlyExport」の「db_API169_MonthlyExport」メソッドを行う,パラメータは「form_code,fiscal_year_code」,戻り値設定は「<result>=result」を設定する。
			
			# form_code
			api169_monthlyexport.formcode = FORM_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fiscal_year_code
			api169_monthlyexport.fiscalyearcode = FISCAL_YEAR_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api169_monthlyexportList = Api169MonthlyexportDao().api169_monthlyexport(api169_monthlyexport)
			api169_monthlyexportlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api169_monthlyexportList != None :
				api169_monthlyexportlistVar = api169_monthlyexportList.fetchall() if hasattr(api169_monthlyexportList, 'fetchall') else api169_monthlyexportList
			if api169_monthlyexportlistVar != None and len(api169_monthlyexportlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api169_monthlyexportlistVar))
			# --LINE114 retrieved first value
			if api169_monthlyexportlistVar != None and len(api169_monthlyexportlistVar) > 0 :
				rec = api169_monthlyexportlistVar[0]
				RESULT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "result")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
