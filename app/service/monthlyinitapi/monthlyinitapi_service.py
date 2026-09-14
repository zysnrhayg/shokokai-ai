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
from app.dao.api128_getmonthlydetail.api128_getmonthlydetail_dao import Api128GetmonthlydetailDao
from app.dao.api129_getmonthlytotal.api129_getmonthlytotal_dao import Api129GetmonthlytotalDao
from app.dao.api130_getexportforms.api130_getexportforms_dao import Api130GetexportformsDao
from app.dto.api108_getfiscalyears.api108_getfiscalyears_dto import Api108GetfiscalyearsDto
from app.dto.api128_getmonthlydetail.api128_getmonthlydetail_dto import Api128GetmonthlydetailDto
from app.dto.api129_getmonthlytotal.api129_getmonthlytotal_dto import Api129GetmonthlytotalDto
from app.dto.api130_getexportforms.api130_getexportforms_dto import Api130GetexportformsDto
from app.dto.monthlyinitapi.monthlyinitapi_dto import MonthlyinitapiDto
from app.service.api108_getfiscalyears.api108_getfiscalyears_service import Api108GetfiscalyearsService
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class MonthlyinitapiService :

	#	# 
	# 月次報告画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def monthlyinitapi(self,monthlyinitapi_dto,jsonObj) :
			
		api128_getmonthlydetail = Api128GetmonthlydetailDto.dict_to_json({}) #CommonFunction 110
		api128_getmonthlydetailList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api128_getmonthlydetail_dto = None #ResultGenerator 119
		#ResultGenerator365
		FILTERGROUP = ""
		YEARMONTH = ""
		SUPPORTCOUNT = ""
		api129_getmonthlytotal = Api129GetmonthlytotalDto.dict_to_json({}) #CommonFunction 110
		api129_getmonthlytotalList = None #ResultGenerator 72
		#_dto api129_getmonthlytotal_dto = None #ResultGenerator 119
		api130_getexportforms = Api130GetexportformsDto.dict_to_json({}) #CommonFunction 110
		api130_getexportformsList = None #ResultGenerator 72
		#_dto api130_getexportforms_dto = None #ResultGenerator 119
		FORMCODE = ""
		SHORTLABEL = ""
		FULLLABEL = ""
		api108_getfiscalyears = Api108GetfiscalyearsDto.dict_to_json({}) #WRFuncEntiryGenerator 60
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#月次報告画面初期表示_MonthlyInitAPI_(API)
			
			#「項目処理」（共通関数:MonthlyInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API128_GetMonthlyDetail」の「db_API128_GetMonthlyDetail」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<filter_group>=filter_group,<year_month>=year_month,<support_count>=support_count」を設定する。
			
			# prefecture_code
			api128_getmonthlydetail.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api128_getmonthlydetail.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api128_getmonthlydetailList = Api128GetmonthlydetailDao().api128_getmonthlydetail(api128_getmonthlydetail)
			api128_getmonthlydetaillistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api128_getmonthlydetailList != None :
				api128_getmonthlydetaillistVar = api128_getmonthlydetailList.fetchall() if hasattr(api128_getmonthlydetailList, 'fetchall') else api128_getmonthlydetailList
			if api128_getmonthlydetaillistVar != None and len(api128_getmonthlydetaillistVar) > 0 :
				SHUTOKUKENSUU = str(len(api128_getmonthlydetaillistVar))
			# --LINE114 retrieved first value
			if api128_getmonthlydetaillistVar != None and len(api128_getmonthlydetaillistVar) > 0 :
				rec = api128_getmonthlydetaillistVar[0]
				FILTERGROUP = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "filter_group")) # ResultGenerator 385
				# ResultGenerator 385
				
				YEARMONTH = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "year_month")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUPPORTCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "support_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API129_GetMonthlyTotal」の「db_API129_GetMonthlyTotal」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<year_month>=year_month,<support_count>=support_count」を設定する。
			
			# prefecture_code
			api129_getmonthlytotal.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api129_getmonthlytotal.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api129_getmonthlytotalList = Api129GetmonthlytotalDao().api129_getmonthlytotal(api129_getmonthlytotal)
			api129_getmonthlytotallistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api129_getmonthlytotalList != None :
				api129_getmonthlytotallistVar = api129_getmonthlytotalList.fetchall() if hasattr(api129_getmonthlytotalList, 'fetchall') else api129_getmonthlytotalList
			if api129_getmonthlytotallistVar != None and len(api129_getmonthlytotallistVar) > 0 :
				SHUTOKUKENSUU = str(len(api129_getmonthlytotallistVar))
			# --LINE114 retrieved first value
			if api129_getmonthlytotallistVar != None and len(api129_getmonthlytotallistVar) > 0 :
				rec = api129_getmonthlytotallistVar[0]
				YEARMONTH = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "year_month")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUPPORTCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "support_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API130_GetExportForms」の「db_API130_GetExportForms」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<form_code>=form_code,<short_label>=short_label,<full_label>=full_label」を設定する。
			
			# fiscal_year_id
			api130_getexportforms.fiscalyearid = FISCAL_YEAR_ID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api130_getexportformsList = Api130GetexportformsDao().api130_getexportforms(api130_getexportforms)
			api130_getexportformslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api130_getexportformsList != None :
				api130_getexportformslistVar = api130_getexportformsList.fetchall() if hasattr(api130_getexportformsList, 'fetchall') else api130_getexportformsList
			if api130_getexportformslistVar != None and len(api130_getexportformslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api130_getexportformslistVar))
			# --LINE114 retrieved first value
			if api130_getexportformslistVar != None and len(api130_getexportformslistVar) > 0 :
				rec = api130_getexportformslistVar[0]
				FORMCODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				SHORTLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "short_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				FULLLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "full_label")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API108_GetFiscalYears」の「db_API108_GetFiscalYears」メソッドを行う,パラメータは「」,戻り値設定は「<fiscal_year_id>=fiscal_year_id,<fiscal_year_code>=fiscal_year_code,<label>=label,<start_month>=start_month,<end_month>=end_month」を設定する。
			api108_getfiscalyears_service = Api108GetfiscalyearsService()
			api108_getfiscalyears_service.db_api108_getfiscalyears(api108_getfiscalyears,jsonObj) #WRFuncEntityGenerator 371
			#WRFuncEntityGenerator 371
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
