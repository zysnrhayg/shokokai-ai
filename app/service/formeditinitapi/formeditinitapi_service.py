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
from app.dao.api119_getreportforms.api119_getreportforms_dao import Api119GetreportformsDao
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api121_getstaffoptions.api121_getstaffoptions_dao import Api121GetstaffoptionsDao
from app.dao.api122_getreportdetail.api122_getreportdetail_dao import Api122GetreportdetailDao
from app.dao.api123_getreportthemes.api123_getreportthemes_dao import Api123GetreportthemesDao
from app.dto.api119_getreportforms.api119_getreportforms_dto import Api119GetreportformsDto
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api121_getstaffoptions.api121_getstaffoptions_dto import Api121GetstaffoptionsDto
from app.dto.api122_getreportdetail.api122_getreportdetail_dto import Api122GetreportdetailDto
from app.dto.api123_getreportthemes.api123_getreportthemes_dto import Api123GetreportthemesDto
from app.dto.formeditinitapi.formeditinitapi_dto import FormeditinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class FormeditinitapiService :

	#	# 
	# 報告書編集画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formeditinitapi(self,formeditinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		PREFECTURE_CODE = formeditinitapi_dto.prefecturecode#GeninusClientScript 1318
		REPORT_ID = formeditinitapi_dto.reportid#GeninusClientScript 1318
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
		api123_getreportthemes = Api123GetreportthemesDto.dict_to_json({}) #CommonFunction 110
		api123_getreportthemesList = None #ResultGenerator 72
		#_dto api123_getreportthemes_dto = None #ResultGenerator 119
		THEMECODE = ""
		LABEL = ""
		api119_getreportforms = Api119GetreportformsDto.dict_to_json({}) #CommonFunction 110
		api119_getreportformsList = None #ResultGenerator 72
		#_dto api119_getreportforms_dto = None #ResultGenerator 119
		FULLLABEL = ""
		SHORTLABEL = ""
		api120_getthemes = Api120GetthemesDto.dict_to_json({}) #CommonFunction 110
		api120_getthemesList = None #ResultGenerator 72
		#_dto api120_getthemes_dto = None #ResultGenerator 119
		FILTERGROUP = ""
		api121_getstaffoptions = Api121GetstaffoptionsDto.dict_to_json({}) #CommonFunction 110
		api121_getstaffoptionsList = None #ResultGenerator 72
		#_dto api121_getstaffoptions_dto = None #ResultGenerator 119
		USERID = ""
		SHOKUINKJ = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集画面初期表示_FormEditInitAPI_(API)
			
			#「項目処理」（共通関数:FormEditInitAPI）,パラメータは（prefecture_code,report_id）
			
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
				
			#関数「API123_GetReportThemes」の「db_API123_GetReportThemes」メソッドを行う,パラメータは「report_id」,戻り値設定は「<theme_id>=theme_id,<theme_code>=theme_code,<label>=label」を設定する。
			
			# report_id
			api123_getreportthemes.reportid = REPORTID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api123_getreportthemesList = Api123GetreportthemesDao().api123_getreportthemes(api123_getreportthemes)
			api123_getreportthemeslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api123_getreportthemesList != None :
				api123_getreportthemeslistVar = api123_getreportthemesList.fetchall() if hasattr(api123_getreportthemesList, 'fetchall') else api123_getreportthemesList
			if api123_getreportthemeslistVar != None and len(api123_getreportthemeslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api123_getreportthemeslistVar))
			# --LINE114 retrieved first value
			if api123_getreportthemeslistVar != None and len(api123_getreportthemeslistVar) > 0 :
				rec = api123_getreportthemeslistVar[0]
				THEMEID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				LABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API119_GetReportForms」の「db_API119_GetReportForms」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<form_code>=form_code,<full_label>=full_label,<short_label>=short_label」を設定する。
			
			# fiscal_year_id
			api119_getreportforms.fiscalyearid = FISCALYEARID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api119_getreportformsList = Api119GetreportformsDao().api119_getreportforms(api119_getreportforms)
			api119_getreportformslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api119_getreportformsList != None :
				api119_getreportformslistVar = api119_getreportformsList.fetchall() if hasattr(api119_getreportformsList, 'fetchall') else api119_getreportformsList
			if api119_getreportformslistVar != None and len(api119_getreportformslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api119_getreportformslistVar))
			# --LINE114 retrieved first value
			if api119_getreportformslistVar != None and len(api119_getreportformslistVar) > 0 :
				rec = api119_getreportformslistVar[0]
				FORMCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FULLLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "full_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHORTLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "short_label")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API120_GetThemes」の「db_API120_GetThemes」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<theme_id>=theme_id,<theme_code>=theme_code,<label>=label,<filter_group>=filter_group」を設定する。
			
			# fiscal_year_id
			api120_getthemes.fiscalyearid = FISCALYEARID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api120_getthemesList = Api120GetthemesDao().api120_getthemes(api120_getthemes)
			api120_getthemeslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api120_getthemesList != None :
				api120_getthemeslistVar = api120_getthemesList.fetchall() if hasattr(api120_getthemesList, 'fetchall') else api120_getthemesList
			if api120_getthemeslistVar != None and len(api120_getthemeslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api120_getthemeslistVar))
			# --LINE114 retrieved first value
			if api120_getthemeslistVar != None and len(api120_getthemeslistVar) > 0 :
				rec = api120_getthemeslistVar[0]
				THEMEID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				LABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")) # ResultGenerator 385
				# ResultGenerator 385
				
				FILTERGROUP = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "filter_group")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API121_GetStaffOptions」の「db_API121_GetStaffOptions」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<user_id>=user_id,<shokuin_kj>=shokuin_kj」を設定する。
			
			# prefecture_code
			api121_getstaffoptions.prefecturecode = PREFECTURECODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api121_getstaffoptions.shokokaicd = SHOKOKAICD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api121_getstaffoptionsList = Api121GetstaffoptionsDao().api121_getstaffoptions(api121_getstaffoptions)
			api121_getstaffoptionslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api121_getstaffoptionsList != None :
				api121_getstaffoptionslistVar = api121_getstaffoptionsList.fetchall() if hasattr(api121_getstaffoptionsList, 'fetchall') else api121_getstaffoptionsList
			if api121_getstaffoptionslistVar != None and len(api121_getstaffoptionslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api121_getstaffoptionslistVar))
			# --LINE114 retrieved first value
			if api121_getstaffoptionslistVar != None and len(api121_getstaffoptionslistVar) > 0 :
				rec = api121_getstaffoptionslistVar[0]
				USERID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKUINKJ = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokuin_kj")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
