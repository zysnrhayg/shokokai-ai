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
from app.dto.aiformatapi.aiformatapi_dto import AiformatapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AiformatapiService :

	#	# 
	# 報告書編集文字起こし AI整形
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aiformatapi(self,aiformatapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		TRANSCRIPT = aiformatapi_dto.transcript  # ONSEIPANERU GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集文字起こし AI整形_AIFORMATAPI_(API)
			
			#「項目処理」（共通関数:AIFORMATAPI）,パラメータは（transcript（音声パネル））
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
