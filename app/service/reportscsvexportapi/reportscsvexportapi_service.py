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
from app.dao.api162_reportscsvexport.api162_reportscsvexport_dao import Api162ReportscsvexportDao
from app.dto.api162_reportscsvexport.api162_reportscsvexport_dto import Api162ReportscsvexportDto
from app.dto.reportscsvexportapi.reportscsvexportapi_dto import ReportscsvexportapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class ReportscsvexportapiService :

	#	# 
	# 報告書一覧（様式F）CSV出力
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def reportscsvexportapi(self,reportscsvexportapi_dto,jsonObj) :
			
		api162_reportscsvexport = Api162ReportscsvexportDto.dict_to_json({}) #CommonFunction 110
		api162_reportscsvexportList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api162_reportscsvexport_dto = None #ResultGenerator 119
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
			#報告書一覧（様式F）CSV出力_ReportsCsvExportAPI_(API)
			
			#「項目処理」（共通関数:ReportsCsvExportAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API162_ReportsCsvExport」の「db_API162_ReportsCsvExport」メソッドを行う,パラメータは「role_prefecture_code,role_shokokai_cd,year_month,fy_start_month,fy_end_month,prefecture_code,shokokai_cd,form,theme,keyword」,戻り値設定は「<report_id>=report_id,<report_code>=report_code,<industry>=industry,<report_date>=report_date,<summary>=summary,<staff_main_name>=staff_main_name,<staff_sub_name>=staff_sub_name,<registered_at>=registered_at,<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<prefecture_name>=prefecture_name,<shokokai_name>=shokokai_name,<theme_label>=theme_label,<theme_badge_class>=theme_badge_class,<theme_filter_group>=theme_filter_group,<form_code>=form_code,<form_short_label>=form_short_label,<form_badge_class>=form_badge_class」を設定する。
			
			# role_prefecture_code
			api162_reportscsvexport.roleprefecturecode = ROLE_PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# role_shokokai_cd
			api162_reportscsvexport.roleshokokaicd = ROLE_SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# year_month
			api162_reportscsvexport.yearmonth = YEAR_MONTH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fy_start_month
			api162_reportscsvexport.fystartmonth = FY_START_MONTH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fy_end_month
			api162_reportscsvexport.fyendmonth = FY_END_MONTH #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# prefecture_code
			api162_reportscsvexport.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api162_reportscsvexport.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# form
			api162_reportscsvexport.form = FORM #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# theme
			api162_reportscsvexport.theme = THEME #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# keyword
			api162_reportscsvexport.keyword = KEYWORD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api162_reportscsvexportList = Api162ReportscsvexportDao().api162_reportscsvexport(api162_reportscsvexport)
			api162_reportscsvexportlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api162_reportscsvexportList != None :
				api162_reportscsvexportlistVar = api162_reportscsvexportList.fetchall() if hasattr(api162_reportscsvexportList, 'fetchall') else api162_reportscsvexportList
			if api162_reportscsvexportlistVar != None and len(api162_reportscsvexportlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api162_reportscsvexportlistVar))
			# --LINE114 retrieved first value
			if api162_reportscsvexportlistVar != None and len(api162_reportscsvexportlistVar) > 0 :
				rec = api162_reportscsvexportlistVar[0]
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
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
