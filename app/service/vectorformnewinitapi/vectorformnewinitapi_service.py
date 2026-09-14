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
from app.dto.vectorformnewinitapi.vectorformnewinitapi_dto import VectorformnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class VectorformnewinitapiService :

	#	# 
	# ベクトルコレクション新規＋ コレクションを登録
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def vectorformnewinitapi(self,vectorformnewinitapi_dto,jsonObj) :
			
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ベクトルコレクション新規＋ コレクションを登録_VectorFormNewInitAPI_(API)
			
			#「項目処理」（共通関数:VectorFormNewInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
