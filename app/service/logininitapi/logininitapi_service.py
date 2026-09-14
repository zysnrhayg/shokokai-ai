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
from app.dao.api_kihonnonshiraseichiran.api_kihonnonshiraseichiran_dao import ApiKihonnonshiraseichiranDao
from app.dto.api100_getprefecturenames.api100_getprefecturenames_dto import Api100GetprefecturenamesDto
from app.dto.api_kihonnonshiraseichiran.api_kihonnonshiraseichiran_dto import ApiKihonnonshiraseichiranDto
from app.dto.logininitapi.logininitapi_dto import LogininitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class LogininitapiService :

	#	# 
	# ログイン画面
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def logininitapi(self,logininitapi_dto,jsonObj) :
			
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
		api_kihonnonshiraseichiran = ApiKihonnonshiraseichiranDto.dict_to_json({}) #CommonFunction 110
		api_kihonnonshiraseichiranList = None #ResultGenerator 72
		#_dto api_kihonnonshiraseichiran_dto = None #ResultGenerator 119
		CONTENT = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ログイン画面_loginInitAPI_(API)
			
			#「項目処理」（共通関数:loginInitAPI）,パラメータは（）
			
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
				
			#関数「API_KihonNoNshiraseIchiran」の「db_API_KihonNoNshiraseIchiran」メソッドを行う,パラメータは「role_code」,戻り値設定は「<content>=content」を設定する。
			
			# role_code
			api_kihonnonshiraseichiran.rolecode = ROLE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api_kihonnonshiraseichiranList = ApiKihonnonshiraseichiranDao().api_kihonnonshiraseichiran(api_kihonnonshiraseichiran)
			api_kihonnonshiraseichiranlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api_kihonnonshiraseichiranList != None :
				api_kihonnonshiraseichiranlistVar = api_kihonnonshiraseichiranList.fetchall() if hasattr(api_kihonnonshiraseichiranList, 'fetchall') else api_kihonnonshiraseichiranList
			if api_kihonnonshiraseichiranlistVar != None and len(api_kihonnonshiraseichiranlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api_kihonnonshiraseichiranlistVar))
			# --LINE114 retrieved first value
			if api_kihonnonshiraseichiranlistVar != None and len(api_kihonnonshiraseichiranlistVar) > 0 :
				rec = api_kihonnonshiraseichiranlistVar[0]
				CONTENT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
