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
from app.dto.api204_formexport.api204_formexport_dto import Api204FormexportDto
from app.dto.formexportapi.formexportapi_dto import FormexportapiDto
from app.service.api204_formexport.api204_formexport_service import Api204FormexportService
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class FormexportapiService :

	#	# 
	# 傾聴内容変換AI帳票出力
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formexportapi(self,formexportapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		FORM_CODE = formexportapi_dto.formcode#GeninusClientScript 1318
		REPORT_ID = formexportapi_dto.report_id#GeninusClientScript 1318
		api204_formexport = Api204FormexportDto.dict_to_json({}) #WRFuncEntiryGenerator 60
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI帳票出力_FORMEXPORTAPI_(API)
			
			#「項目処理」（共通関数:FORMEXPORTAPI）,パラメータは（form_code,report_id任意）
			
			#以下の処理を行う。
			
			#関数「API204_FORMEXPORT」の「db_API204_FORMEXPORT」メソッドを行う,パラメータは「report_id」,戻り値設定は「<report_id>=report_id,<report_code>=report_code,<form_code>=form_code,<form_full_label>=form_full_label,<report_date>=report_date,<time_start>=time_start,<time_end>=time_end,<staff_main_name>=staff_main_name,<staff_sub_name>=staff_sub_name,<industry>=industry,<business_name>=business_name,<business_person>=business_person,<content>=content,<summary>=summary,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd」を設定する。
			api204_formexport_service = Api204FormexportService()
			api204_formexport_service.db_api204_formexport(api204_formexport,jsonObj) #WRFuncEntityGenerator 371
			#WRFuncEntityGenerator 371
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
