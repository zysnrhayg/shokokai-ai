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
from app.dto.api119_getreportforms.api119_getreportforms_dto import Api119GetreportformsDto
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api121_getstaffoptions.api121_getstaffoptions_dto import Api121GetstaffoptionsDto
from app.dto.formnewinitapi.formnewinitapi_dto import FormnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class FormnewinitapiService :

	#	# 
	# 報告書新規画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formnewinitapi(self,formnewinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		PREFILL = formnewinitapi_dto.prefill#GeninusClientScript 1318
		api119_getreportforms = Api119GetreportformsDto.dict_to_json({}) #CommonFunction 110
		api119_getreportformsList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api119_getreportforms_dto = None #ResultGenerator 119
		#ResultGenerator365
		FORMCODE = ""
		FULLLABEL = ""
		SHORTLABEL = ""
		api120_getthemes = Api120GetthemesDto.dict_to_json({}) #CommonFunction 110
		api120_getthemesList = None #ResultGenerator 72
		#_dto api120_getthemes_dto = None #ResultGenerator 119
		THEMEID = ""
		THEMECODE = ""
		LABEL = ""
		FILTERGROUP = ""
		api121_getstaffoptions = Api121GetstaffoptionsDto.dict_to_json({}) #CommonFunction 110
		api121_getstaffoptionsList = None #ResultGenerator 72
		#_dto api121_getstaffoptions_dto = None #ResultGenerator 119
		USERID = ""
		SHOKUINKJ = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書新規画面初期表示_FormNewInitAPI_(API)
			
			#「項目処理」（共通関数:FormNewInitAPI）,パラメータは（prefill）
			
			#以下の処理を行う。
			
			#関数「API119_GetReportForms」の「db_API119_GetReportForms」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<form_code>=form_code,<full_label>=full_label,<short_label>=short_label」を設定する。
			
			# fiscal_year_id
			api119_getreportforms.fiscalyearid = FISCAL_YEAR_ID #ArgumentGenerator 274
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
			api120_getthemes.fiscalyearid = FISCAL_YEAR_ID #ArgumentGenerator 274
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
			api121_getstaffoptions.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api121_getstaffoptions.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
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
		
			
	
	
