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
from app.dao.api118_getreports.api118_getreports_dao import Api118GetreportsDao
from app.dto.api118_getreports.api118_getreports_dto import Api118GetreportsDto
from app.dto.reportssearchapi.reportssearchapi_dto import ReportssearchapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class ReportssearchapiService :

	#	# 
	# 報告書一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def reportssearchapi(self,reportssearchapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		DEFAULT_FORM = reportssearchapi_dto.defaultform#GeninusClientScript 1318
		api118_getreports = Api118GetreportsDto.dict_to_json({}) #CommonFunction 110
		api118_getreportsList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api118_getreports_dto = None #ResultGenerator 119
		#ResultGenerator365
		REPORTID = ""
		REPORTCODE = ""
		INDUSTRY = ""
		REPORTDATE = ""
		SUMMARY = ""
		STAFFMAINNAME = ""
		STAFFSUBNAME = ""
		REGISTEREDAT = ""
		PREFECTURECODE = ""
		SHOKOKAICD = ""
		PREFECTURENAME = ""
		SHOKOKAINAME = ""
		THEMELABEL = ""
		THEMEBADGECLASS = ""
		THEMEFILTERGROUP = ""
		FORMCODE = ""
		FORMSHORTLABEL = ""
		FORMBADGECLASS = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書一覧画面初期表示_ReportsSearchAPI_(API)
			
			#「項目処理」（共通関数:ReportsSearchAPI）,パラメータは（default_form）
			
			#以下の処理を行う。
			
			#関数「API118_GetReports」の「db_API118_GetReports」メソッドを行う,パラメータは「role_prefecture_code,role_shokokai_cd,year_month,fy_start_month,fy_end_month,prefecture_code,shokokai_cd,form,theme,keyword」,戻り値設定は「<report_id>=report_id,<report_code>=report_code,<industry>=industry,<report_date>=report_date,<summary>=summary,<staff_main_name>=staff_main_name,<staff_sub_name>=staff_sub_name,<registered_at>=registered_at,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<prefecture_name>=prefecture_name,<shokokai_name>=shokokai_name,<theme_label>=theme_label,<theme_badge_class>=theme_badge_class,<theme_filter_group>=theme_filter_group,<form_code>=form_code,<form_short_label>=form_short_label,<form_badge_class>=form_badge_class」を設定する。
			
			# role_prefecture_code
			api118_getreports.roleprefecturecode = ROLE_PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# role_shokokai_cd
			api118_getreports.roleshokokaicd = ROLE_SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# year_month
			api118_getreports.yearmonth = YEAR_MONTH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fy_start_month
			api118_getreports.fystartmonth = FY_START_MONTH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fy_end_month
			api118_getreports.fyendmonth = FY_END_MONTH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api118_getreports.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api118_getreports.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# form
			api118_getreports.form = FORM #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# theme
			api118_getreports.theme = THEME #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# keyword
			api118_getreports.keyword = KEYWORD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api118_getreportsList = Api118GetreportsDao().api118_getreports(api118_getreports)
			api118_getreportslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api118_getreportsList != None :
				api118_getreportslistVar = api118_getreportsList.fetchall() if hasattr(api118_getreportsList, 'fetchall') else api118_getreportsList
			if api118_getreportslistVar != None and len(api118_getreportslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api118_getreportslistVar))
			# --LINE114 retrieved first value
			if api118_getreportslistVar != None and len(api118_getreportslistVar) > 0 :
				rec = api118_getreportslistVar[0]
				REPORTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				INDUSTRY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "industry")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUMMARY = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "summary")) # ResultGenerator 385
				# ResultGenerator 385
				
				STAFFMAINNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "staff_main_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				STAFFSUBNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "staff_sub_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				REGISTEREDAT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "registered_at")) # ResultGenerator 385
				# ResultGenerator 385
				
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAICD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")) # ResultGenerator 385
				# ResultGenerator 385
				
				PREFECTURENAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAINAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMELABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMEBADGECLASS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_badge_class")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMEFILTERGROUP = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_filter_group")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMSHORTLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_short_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMBADGECLASS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_badge_class")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API118_GetReports」の「db_API118_GetReports」取得結果をGrid「reports-tbody」に設定する。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api118_getreportslistVar != None and len(api118_getreportslistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api118_getreportslistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api118_getreportslistVar[i]
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
		
			
	
	
