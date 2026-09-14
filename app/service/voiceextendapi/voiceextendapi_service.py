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
from app.dto.voiceextendapi.voiceextendapi_dto import VoiceextendapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VoiceextendapiService :

	#	# 
	# 報告書編集録音時間 ＋30分延長
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def voiceextendapi(self,voiceextendapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		REPORT_ID = voiceextendapi_dto.reportid  # 任意 GeninusClientScript 1318
		ADD_SECONDS = voiceextendapi_dto.addseconds#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集録音時間 ＋30分延長_VOICEEXTENDAPI_(API)
			
			#「項目処理」（共通関数:VOICEEXTENDAPI）,パラメータは（report_id任意,add_seconds）
			
			#以下の処理を行う。
			
			#タイマーを延長しtimer_remaining/timer_totalを返す。
			#タイマーを延長しtimer_remaining/timer_totalを返す。
			pass
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
