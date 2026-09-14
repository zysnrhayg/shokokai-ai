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
from app.dao.api125_insertreporttheme.api125_insertreporttheme_dao import Api125InsertreportthemeDao
from app.dao.api126_updatereport.api126_updatereport_dao import Api126UpdatereportDao
from app.dao.api127_deletereportthemes.api127_deletereportthemes_dao import Api127DeletereportthemesDao
from app.dto.api125_insertreporttheme.api125_insertreporttheme_dto import Api125InsertreportthemeDto
from app.dto.api126_updatereport.api126_updatereport_dto import Api126UpdatereportDto
from app.dto.api127_deletereportthemes.api127_deletereportthemes_dto import Api127DeletereportthemesDto
from app.dto.formeditsaveapi.formeditsaveapi_dto import FormeditsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class FormeditsaveapiService :

	#	# 
	# 報告書編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formeditsaveapi(self,formeditsaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		REPORT_ID = formeditsaveapi_dto.reportid#GeninusClientScript 1318
		FORM_CODE = formeditsaveapi_dto.formcode#GeninusClientScript 1318
		REPORT_DATE = formeditsaveapi_dto.reportdate#GeninusClientScript 1318
		TIME_START = formeditsaveapi_dto.timestart#GeninusClientScript 1318
		TIME_END = formeditsaveapi_dto.timeend#GeninusClientScript 1318
		STAFF_MAIN_CODE = formeditsaveapi_dto.staffmaincode#GeninusClientScript 1318
		STAFF_SUB_CODE = formeditsaveapi_dto.staffsubcode#GeninusClientScript 1318
		THEME_CODES = formeditsaveapi_dto.themecodes#GeninusClientScript 1318
		INDUSTRY = formeditsaveapi_dto.industry#GeninusClientScript 1318
		BUSINESS_NAME = formeditsaveapi_dto.businessname#GeninusClientScript 1318
		BUSINESS_PERSON = formeditsaveapi_dto.businessperson#GeninusClientScript 1318
		CONTENT = formeditsaveapi_dto.content#GeninusClientScript 1318
		SUMMARY = formeditsaveapi_dto.summary#GeninusClientScript 1318
		STATUS = formeditsaveapi_dto.status#GeninusClientScript 1318
		THEME_ID = formeditsaveapi_dto.themeid#GeninusClientScript 1318
		api126_updatereport = Api126UpdatereportDto.dict_to_json({}) #CommonFunction 110
		api127_deletereportthemes = Api127DeletereportthemesDto.dict_to_json({}) #CommonFunction 110
		api125_insertreporttheme = Api125InsertreportthemeDto.dict_to_json({}) #CommonFunction 110
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集画面登録ボタン_FormEditSaveAPI_(API)
			
			#「項目処理」（共通関数:FormEditSaveAPI）,パラメータは（report_id,form_code,report_date,time_start,time_end,staff_main_code,staff_sub_code,theme_codes,industry,business_name,business_person,content,summary,status,theme_id）
			
			#以下の処理を行う。
			
			#関数「API126_UpdateReport」の「db_API126_UpdateReport」メソッドを行う,パラメータは「form_code,fiscal_year_id,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status,report_id」。
			
			# form_code
			api126_updatereport.formcode = FORM_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fiscal_year_id
			api126_updatereport.fiscalyearid = FISCAL_YEAR_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# theme_id
			api126_updatereport.themeid = THEME_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# industry
			api126_updatereport.industry = INDUSTRY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# report_date
			api126_updatereport.reportdate = REPORT_DATE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# summary
			api126_updatereport.summary = SUMMARY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# content
			api126_updatereport.content = CONTENT #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# time_start
			api126_updatereport.timestart = TIME_START #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# time_end
			api126_updatereport.timeend = TIME_END #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# business_person
			api126_updatereport.businessperson = BUSINESS_PERSON #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# business_name
			api126_updatereport.businessname = BUSINESS_NAME #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# staff_main_name
			api126_updatereport.staffmainname = STAFF_MAIN_NAME #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# staff_sub_name
			api126_updatereport.staffsubname = STAFF_SUB_NAME #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# status
			api126_updatereport.status = STATUS #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# report_id
			api126_updatereport.reportid = REPORT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			Api126UpdatereportDao().api126_updatereport(api126_updatereport) #ResultGenerator 104
			#ResultGenerator 104
			#関数「API127_DeleteReportThemes」の「db_API127_DeleteReportThemes」メソッドを行う,パラメータは「report_id」。
			
			# report_id
			api127_deletereportthemes.reportid = REPORT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			Api127DeletereportthemesDao().api127_deletereportthemes(api127_deletereportthemes) #ResultGenerator 104
			#ResultGenerator 104
			#関数「API125_InsertReportTheme」の「db_API125_InsertReportTheme」メソッドを行う,パラメータは「report_id,theme_id」。
			
			# report_id
			api125_insertreporttheme.reportid = REPORT_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# theme_id
			api125_insertreporttheme.themeid = THEME_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			Api125InsertreportthemeDao().api125_insertreporttheme(api125_insertreporttheme) #ResultGenerator 104
			#ResultGenerator 104
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
