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
from app.dto.voicerecordapi.voicerecordapi_dto import VoicerecordapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VoicerecordapiService :

	#	# 
	# 傾聴内容変換AI音声録音 開始／停止
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def voicerecordapi(self,voicerecordapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		ACTION = voicerecordapi_dto.action#start|stop #GeninusClientScript 1318
		REPORT_ID = voicerecordapi_dto.report_id#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI音声録音 開始／停止_VOICERECORDAPI_(API)
			
			#「項目処理」（共通関数:VOICERECORDAPI）,パラメータは（action=start|stop,report_id任意）
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
