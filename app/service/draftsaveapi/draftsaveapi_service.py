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
from app.dto.draftsaveapi.draftsaveapi_dto import DraftsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DraftsaveapiService :

	#	# 
	# 傾聴内容変換AI下書き保存
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def draftsaveapi(self,draftsaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		HOUKOKUSHOKOUMOKUISSHIKI = draftsaveapi_dto.houkokushokoumokuisshiki#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI下書き保存_DRAFTSAVEAPI_(API)
			
			#「項目処理」（共通関数:DRAFTSAVEAPI）,パラメータは（報告書項目一式）
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
