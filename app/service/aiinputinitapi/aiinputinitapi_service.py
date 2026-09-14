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
from app.dto.aiinputinitapi.aiinputinitapi_dto import AiinputinitapiDto
from app.dto.api119_getreportforms.api119_getreportforms_dto import Api119GetreportformsDto
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api121_getstaffoptions.api121_getstaffoptions_dto import Api121GetstaffoptionsDto
from app.service.api119_getreportforms.api119_getreportforms_service import Api119GetreportformsService
from app.service.api120_getthemes.api120_getthemes_service import Api120GetthemesService
from app.service.api121_getstaffoptions.api121_getstaffoptions_service import Api121GetstaffoptionsService
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AiinputinitapiService :

	#	# 
	# 傾聴内容変換AI画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aiinputinitapi(self,aiinputinitapi_dto,jsonObj) :
			
		api119_getreportforms = Api119GetreportformsDto.dict_to_json({}) #WRFuncEntiryGenerator 60
		api120_getthemes = Api120GetthemesDto.dict_to_json({}) #WRFuncEntiryGenerator 60
		api121_getstaffoptions = Api121GetstaffoptionsDto.dict_to_json({}) #WRFuncEntiryGenerator 60
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI画面初期表示_AiInputInitAPI_(API)
			
			#「項目処理」（共通関数:AiInputInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#関数「API119_GetReportForms」の「db_API119_GetReportForms」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<form_code>=form_code,<full_label>=full_label,<short_label>=short_label」を設定する。
			api119_getreportforms_service = Api119GetreportformsService()
			api119_getreportforms_service.db_api119_getreportforms(api119_getreportforms,jsonObj) #WRFuncEntityGenerator 371
			#WRFuncEntityGenerator 371
			#関数「API120_GetThemes」の「db_API120_GetThemes」メソッドを行う,パラメータは「fiscal_year_id」,戻り値設定は「<theme_id>=theme_id,<theme_code>=theme_code,<label>=label,<filter_group>=filter_group」を設定する。
			api120_getthemes_service = Api120GetthemesService()
			api120_getthemes_service.db_api120_getthemes(api120_getthemes,jsonObj) #WRFuncEntityGenerator 371
			#WRFuncEntityGenerator 371
			#関数「API121_GetStaffOptions」の「db_API121_GetStaffOptions」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<user_id>=user_id,<shokuin_kj>=shokuin_kj」を設定する。
			api121_getstaffoptions_service = Api121GetstaffoptionsService()
			api121_getstaffoptions_service.db_api121_getstaffoptions(api121_getstaffoptions,jsonObj) #WRFuncEntityGenerator 371
			#WRFuncEntityGenerator 371
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
