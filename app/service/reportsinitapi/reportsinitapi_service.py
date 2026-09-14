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
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dao.api102_getshokokai.api102_getshokokai_dao import Api102GetshokokaiDao
from app.dao.api108_getfiscalyears.api108_getfiscalyears_dao import Api108GetfiscalyearsDao
from app.dao.api118_getreports.api118_getreports_dao import Api118GetreportsDao
from app.dao.getreportforms.getreportforms_dao import GetreportformsDao
from app.dao.getthemegroups.getthemegroups_dao import GetthemegroupsDao
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto
from app.dto.api102_getshokokai.api102_getshokokai_dto import Api102GetshokokaiDto
from app.dto.api108_getfiscalyears.api108_getfiscalyears_dto import Api108GetfiscalyearsDto
from app.dto.api118_getreports.api118_getreports_dto import Api118GetreportsDto
from app.dto.getreportforms.getreportforms_dto import GetreportformsDto
from app.dto.getthemegroups.getthemegroups_dto import GetthemegroupsDto
from app.dto.reportsinitapi.reportsinitapi_dto import ReportsinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class ReportsinitapiService :

	#	# 
	# 報告書一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def reportsinitapi(self,reportsinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		DEFAULT_FORM = reportsinitapi_dto.defaultform#GeninusClientScript 1318
		api108_getfiscalyears = Api108GetfiscalyearsDto.dict_to_json({}) #CommonFunction 110
		api108_getfiscalyearsList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api108_getfiscalyears_dto = None #ResultGenerator 119
		#ResultGenerator365
		FISCALYEARID = ""
		FISCALYEARCODE = ""
		LABEL = ""
		STARTMONTH = ""
		ENDMONTH = ""
		api100_getprefecturenames = Api100GetprefecturenamesDto.dict_to_json({}) #CommonFunction 110
		api100_getprefecturenamesList = None #ResultGenerator 72
		#_dto api100_getprefecturenames_dto = None #ResultGenerator 119
		PREFECTURECODE = ""
		NAME = ""
		SHORTNAME = ""
		REGION = ""
		SORTORDER = ""
		ISPSEUDO = ""
		api102_getshokokai = Api102GetshokokaiDto.dict_to_json({}) #CommonFunction 110
		api102_getshokokaiList = None #ResultGenerator 72
		#_dto api102_getshokokai_dto = None #ResultGenerator 119
		SHOKOKAICD = ""
		getreportforms = GetreportformsDto.dict_to_json({}) #CommonFunction 110
		getreportformsList = None #ResultGenerator 72
		#_dto getreportforms_dto = None #ResultGenerator 119
		FORMCODE = ""
		FULLLABEL = ""
		getthemegroups = GetthemegroupsDto.dict_to_json({}) #CommonFunction 110
		getthemegroupsList = None #ResultGenerator 72
		#_dto getthemegroups_dto = None #ResultGenerator 119
		FILTERGROUP = ""
		FILTERGROUPLABEL = ""
		api118_getreports = Api118GetreportsDto.dict_to_json({}) #CommonFunction 110
		api118_getreportsList = None #ResultGenerator 72
		#_dto api118_getreports_dto = None #ResultGenerator 119
		REPORTID = ""
		REPORTCODE = ""
		INDUSTRY = ""
		REPORTDATE = ""
		SUMMARY = ""
		STAFFMAINNAME = ""
		STAFFSUBNAME = ""
		REGISTEREDAT = ""
		PREFECTURENAME = ""
		SHOKOKAINAME = ""
		THEMELABEL = ""
		THEMEBADGECLASS = ""
		THEMEFILTERGROUP = ""
		FORMSHORTLABEL = ""
		FORMBADGECLASS = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書一覧画面初期表示_ReportsInitAPI_(API)
			
			#「項目処理」（共通関数:ReportsInitAPI）,パラメータは（default_form）
			
			#以下の処理を行う。
			
			#関数「API108_GetFiscalYears」の「db_API108_GetFiscalYears」メソッドを行う,パラメータは「」,戻り値設定は「<fiscal_year_id>=fiscal_year_id,<fiscal_year_code>=fiscal_year_code,<label>=label,<start_month>=start_month,<end_month>=end_month」を設定する。
			
			#ReulstGenerator 87
			api108_getfiscalyearsList = Api108GetfiscalyearsDao().api108_getfiscalyears(api108_getfiscalyears)
			api108_getfiscalyearslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api108_getfiscalyearsList != None :
				api108_getfiscalyearslistVar = api108_getfiscalyearsList.fetchall() if hasattr(api108_getfiscalyearsList, 'fetchall') else api108_getfiscalyearsList
			if api108_getfiscalyearslistVar != None and len(api108_getfiscalyearslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api108_getfiscalyearslistVar))
			# --LINE114 retrieved first value
			if api108_getfiscalyearslistVar != None and len(api108_getfiscalyearslistVar) > 0 :
				rec = api108_getfiscalyearslistVar[0]
				FISCALYEARID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "fiscal_year_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				FISCALYEARCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "fiscal_year_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				LABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")) # ResultGenerator 385
				# ResultGenerator 385
				
				STARTMONTH = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "start_month")) # ResultGenerator 385
				# ResultGenerator 385
				
				ENDMONTH = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "end_month")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API100_GetPrefectureNames」の「db_API100_GetPrefectureNames」メソッドを行う,パラメータは「」,戻り値設定は「<prefecture_code>=prefecture_code,<name>=name,<short_name>=short_name,<region>=region,<sort_order>=sort_order,<is_pseudo>=is_pseudo」を設定する。
			
			#ReulstGenerator 87
			api100_getprefecturenamesList = Api100GetprefecturenamesDao().api100_getprefecturenames(api100_getprefecturenames)
			api100_getprefecturenameslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api100_getprefecturenamesList != None :
				api100_getprefecturenameslistVar = api100_getprefecturenamesList.fetchall() if hasattr(api100_getprefecturenamesList, 'fetchall') else api100_getprefecturenamesList
			if api100_getprefecturenameslistVar != None and len(api100_getprefecturenameslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api100_getprefecturenameslistVar))
			# --LINE114 retrieved first value
			if api100_getprefecturenameslistVar != None and len(api100_getprefecturenameslistVar) > 0 :
				rec = api100_getprefecturenameslistVar[0]
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHORTNAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "short_name")) # ResultGenerator 385
				# ResultGenerator 385
				
				REGION = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "region")) # ResultGenerator 385
				# ResultGenerator 385
				
				SORTORDER = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "sort_order")) # ResultGenerator 385
				# ResultGenerator 385
				
				ISPSEUDO = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "is_pseudo")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API102_GetShokokai」の「db_API102_GetShokokai」メソッドを行う,パラメータは「prefecture_code,only_federation,exclude_federation」,戻り値設定は「<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<name>=name」を設定する。
			
			# prefecture_code
			api102_getshokokai.prefecturecode = PREFECTURECODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# only_federation
			api102_getshokokai.onlyfederation = ONLY_FEDERATION #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# exclude_federation
			api102_getshokokai.excludefederation = EXCLUDE_FEDERATION #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api102_getshokokaiList = Api102GetshokokaiDao().api102_getshokokai(api102_getshokokai)
			api102_getshokokailistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api102_getshokokaiList != None :
				api102_getshokokailistVar = api102_getshokokaiList.fetchall() if hasattr(api102_getshokokaiList, 'fetchall') else api102_getshokokaiList
			if api102_getshokokailistVar != None and len(api102_getshokokailistVar) > 0 :
				SHUTOKUKENSUU = str(len(api102_getshokokailistVar))
			# --LINE114 retrieved first value
			if api102_getshokokailistVar != None and len(api102_getshokokailistVar) > 0 :
				rec = api102_getshokokailistVar[0]
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHOKOKAICD = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokokai_cd")) # ResultGenerator 385
				# ResultGenerator 385
				
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「GetReportForms」の「db_GetReportForms」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<form_code>=form_code,<full_label>=full_label」を設定する。
			
			# fiscal_year_id
			getreportforms.fiscalyearid = FISCALYEARID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			getreportformsList = GetreportformsDao().getreportforms(getreportforms)
			getreportformslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if getreportformsList != None :
				getreportformslistVar = getreportformsList.fetchall() if hasattr(getreportformsList, 'fetchall') else getreportformsList
			if getreportformslistVar != None and len(getreportformslistVar) > 0 :
				SHUTOKUKENSUU = str(len(getreportformslistVar))
			# --LINE114 retrieved first value
			if getreportformslistVar != None and len(getreportformslistVar) > 0 :
				rec = getreportformslistVar[0]
				FORMCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				FULLLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "full_label")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「GetThemeGroups」の「db_GetThemeGroups」メソッドを行う,パラメータは「」,戻り値設定は「<filter_group>=filter_group,<filter_group_label>=filter_group_label」を設定する。
			
			#ReulstGenerator 87
			getthemegroupsList = GetthemegroupsDao().getthemegroups(getthemegroups)
			getthemegroupslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if getthemegroupsList != None :
				getthemegroupslistVar = getthemegroupsList.fetchall() if hasattr(getthemegroupsList, 'fetchall') else getthemegroupsList
			if getthemegroupslistVar != None and len(getthemegroupslistVar) > 0 :
				SHUTOKUKENSUU = str(len(getthemegroupslistVar))
			# --LINE114 retrieved first value
			if getthemegroupslistVar != None and len(getthemegroupslistVar) > 0 :
				rec = getthemegroupslistVar[0]
				FILTERGROUP = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "filter_group")) # ResultGenerator 385
				# ResultGenerator 385
				
				FILTERGROUPLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "filter_group_label")) # ResultGenerator 385
				# ResultGenerator 385
				
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
			api118_getreports.prefecturecode = PREFECTURECODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api118_getreports.shokokaicd = SHOKOKAICD #ArgumentGenerator 274
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
		
			
	
	
