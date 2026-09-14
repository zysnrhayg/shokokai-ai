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
from app.dao.api204_formexport.api204_formexport_dao import Api204FormexportDao
from app.dto.api204_formexport.api204_formexport_dto import Api204FormexportDto
from app.dto.formexportapi.formexportapi_dto import FormexportapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class FormexportapiService :

	#	# 
	# 報告書新規帳票出力
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formexportapi(self,formexportapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		FORM_CODE = formexportapi_dto.formcode#GeninusClientScript 1318
		REPORT_ID = formexportapi_dto.reportid  # 任意 GeninusClientScript 1318
		api204_formexport = Api204FormexportDto.dict_to_json({}) #CommonFunction 110
		api204_formexportList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api204_formexport_dto = None #ResultGenerator 119
		#ResultGenerator365
		REPORTID = ""
		REPORTCODE = ""
		FORMCODE = ""
		FORMFULLLABEL = ""
		REPORTDATE = ""
		TIMESTART = ""
		TIMEEND = ""
		STAFFMAINNAME = ""
		STAFFSUBNAME = ""
		INDUSTRY = ""
		BUSINESSNAME = ""
		BUSINESSPERSON = ""
		CONTENT = ""
		SUMMARY = ""
		PREFECTURECODE = ""
		SHOKOKAICD = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書新規帳票出力_FORMEXPORTAPI_(API)
			
			#「項目処理」（共通関数:FORMEXPORTAPI）,パラメータは（form_code,report_id任意）
			
			#以下の処理を行う。
			
			#関数「API204_FORMEXPORT」の「db_API204_FORMEXPORT」メソッドを行う,パラメータは「report_id」,戻り値設定は「<report_id>=report_id,<report_code>=report_code,<form_code>=form_code,<form_full_label>=form_full_label,<report_date>=report_date,<time_start>=time_start,<time_end>=time_end,<staff_main_name>=staff_main_name,<staff_sub_name>=staff_sub_name,<industry>=industry,<business_name>=business_name,<business_person>=business_person,<content>=content,<summary>=summary,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd」を設定する。
			
			# report_id
			api204_formexport.reportid = REPORT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api204_formexportList = Api204FormexportDao().api204_formexport(api204_formexport)
			api204_formexportlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api204_formexportList != None :
				api204_formexportlistVar = api204_formexportList.fetchall() if hasattr(api204_formexportList, 'fetchall') else api204_formexportList
			if api204_formexportlistVar != None and len(api204_formexportlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api204_formexportlistVar))
			# --LINE114 retrieved first value
			if api204_formexportlistVar != None and len(api204_formexportlistVar) > 0 :
				rec = api204_formexportlistVar[0]
				REPORTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMFULLLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_full_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				TIMESTART = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "time_start")) # ResultGenerator 385
				# ResultGenerator 385
				
				TIMEEND = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "time_end")) # ResultGenerator 385
				# ResultGenerator 385
				
				STAFFMAINNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "staff_main_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				STAFFSUBNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "staff_sub_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				INDUSTRY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "industry")) # ResultGenerator 385
				# ResultGenerator 385
				
				BUSINESSNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "business_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				BUSINESSPERSON = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "business_person")) # ResultGenerator 385
				# ResultGenerator 385
				
				CONTENT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUMMARY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "summary")) # ResultGenerator 385
				# ResultGenerator 385
				
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAICD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
