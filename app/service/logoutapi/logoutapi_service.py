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
from app.dto.logoutapi.logoutapi_dto import LogoutapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class LogoutapiService :

	#	# 
	# ログアウト
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def logoutapi(self,logoutapi_dto,jsonObj) :
			
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ログアウト_LogoutAPI_(API)
			
			#「項目処理」（共通関数:LogoutAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
