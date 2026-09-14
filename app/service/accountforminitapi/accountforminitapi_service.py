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
from app.dto.accountforminitapi.accountforminitapi_dto import AccountforminitapiDto
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto
from app.dto.api102_getshokokai.api102_getshokokai_dto import Api102GetshokokaiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AccountforminitapiService :

	#	# 
	# アカウント新規画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def accountforminitapi(self,accountforminitapi_dto,jsonObj) :
			
		api100_getprefecturenames = Api100GetprefecturenamesDto.dict_to_json({}) #CommonFunction 110
		api100_getprefecturenamesList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api100_getprefecturenames_dto = None #ResultGenerator 119
		#ResultGenerator365
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
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#アカウント新規画面初期表示_AccountFormInitAPI_(API)
			
			#「項目処理」（共通関数:AccountFormInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
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
				
			#関数「API102_GetShokokai」の「db_API102_GetShokokai」メソッドを行う,パラメータは「」,戻り値設定は「<prefecture_code>=prefecture_code,<shokokai_cd>=shokokai_cd,<name>=name」を設定する。
			
			# prefecture_code
			api102_getshokokai.prefecturecode = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# only_federation
			api102_getshokokai.onlyfederation = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
			# exclude_federation
			api102_getshokokai.excludefederation = "" #ArgumentGenerator 237
			#ArgumentGenerator 237
			
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
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
