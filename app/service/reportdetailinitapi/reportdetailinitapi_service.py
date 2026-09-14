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
from app.dao.api122_getreportdetail.api122_getreportdetail_dao import Api122GetreportdetailDao
from app.dto.api122_getreportdetail.api122_getreportdetail_dto import Api122GetreportdetailDto
from app.dto.reportdetailinitapi.reportdetailinitapi_dto import ReportdetailinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class ReportdetailinitapiService :

	#	# 
	# 報告書詳細画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def reportdetailinitapi(self,reportdetailinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		REPORT_ID = reportdetailinitapi_dto.reportid#GeninusClientScript 1318
		api122_getreportdetail = Api122GetreportdetailDto.dict_to_json({}) #CommonFunction 110
		api122_getreportdetailList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api122_getreportdetail_dto = None #ResultGenerator 119
		#ResultGenerator365
		REPORTID = ""
		REPORTCODE = ""
		FORMCODE = ""
		FISCALYEARID = ""
		PREFECTURECODE = ""
		SHOKOKAICD = ""
		THEMEID = ""
		INDUSTRY = ""
		REPORTDATE = ""
		SUMMARY = ""
		CONTENT = ""
		TIMESTART = ""
		TIMEEND = ""
		BUSINESSPERSON = ""
		BUSINESSNAME = ""
		STAFFMAINNAME = ""
		STAFFSUBNAME = ""
		REGISTEREDAT = ""
		FORMFULLLABEL = ""
		PRIMARYTHEMECODE = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書詳細画面初期表示_ReportDetailInitAPI_(API)
			
			#「項目処理」（共通関数:ReportDetailInitAPI）,パラメータは（report_id）
			
			#以下の処理を行う。
			
			#関数「API122_GetReportDetail」の「db_API122_GetReportDetail」メソッドを行う,パラメータは「report_id」,戻り値設定は「<report_id>=report_id,<report_code>=report_code,<form_code>=form_code,<fiscal_year_id>=fiscal_year_id,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<theme_id>=theme_id,<industry>=industry,<report_date>=report_date,<summary>=summary,<content>=content,<time_start>=time_start,<time_end>=time_end,<business_person>=business_person,<business_name>=business_name,<staff_main_name>=staff_main_name,<staff_sub_name>=staff_sub_name,<registered_at>=registered_at,<form_full_label>=form_full_label,<primary_theme_code>=primary_theme_code」を設定する。
			
			# report_id
			api122_getreportdetail.reportid = REPORT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api122_getreportdetailList = Api122GetreportdetailDao().api122_getreportdetail(api122_getreportdetail)
			api122_getreportdetaillistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api122_getreportdetailList != None :
				api122_getreportdetaillistVar = api122_getreportdetailList.fetchall() if hasattr(api122_getreportdetailList, 'fetchall') else api122_getreportdetailList
			if api122_getreportdetaillistVar != None and len(api122_getreportdetaillistVar) > 0 :
				SHUTOKUKENSUU = str(len(api122_getreportdetaillistVar))
			# --LINE114 retrieved first value
			if api122_getreportdetaillistVar != None and len(api122_getreportdetaillistVar) > 0 :
				rec = api122_getreportdetaillistVar[0]
				REPORTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FISCALYEARID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "fiscal_year_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAICD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMEID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				INDUSTRY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "industry")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUMMARY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "summary")) # ResultGenerator 385
				# ResultGenerator 385
				
				CONTENT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content")) # ResultGenerator 385
				# ResultGenerator 385
				
				TIMESTART = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "time_start")) # ResultGenerator 385
				# ResultGenerator 385
				
				TIMEEND = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "time_end")) # ResultGenerator 385
				# ResultGenerator 385
				
				BUSINESSPERSON = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "business_person")) # ResultGenerator 385
				# ResultGenerator 385
				
				BUSINESSNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "business_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				STAFFMAINNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "staff_main_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				STAFFSUBNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "staff_sub_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				REGISTEREDAT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "registered_at")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMFULLLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_full_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				PRIMARYTHEMECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "primary_theme_code")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
