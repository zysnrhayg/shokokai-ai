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
from app.dto.aisummarizeapi.aisummarizeapi_dto import AisummarizeapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class AisummarizeapiService :

	#	# 
	# 報告書編集内容 AI要約→概要反映
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aisummarizeapi(self,aisummarizeapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		CONTENT = aisummarizeapi_dto.content#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集内容 AI要約→概要反映_AISUMMARIZEAPI_(API)
			
			#「項目処理」（共通関数:AISUMMARIZEAPI）,パラメータは（content）
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
