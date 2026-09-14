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
from app.dto.documentformnewinitapi.documentformnewinitapi_dto import DocumentformnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DocumentformnewinitapiService :

	#	# 
	# ナレッジ文書新規＋ 文書を登録
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentformnewinitapi(self,documentformnewinitapi_dto,jsonObj) :
			
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書新規＋ 文書を登録_DocumentFormNewInitAPI_(API)
			
			#「項目処理」（共通関数:DocumentFormNewInitAPI）,パラメータは（）
			
			#以下の処理を行う。
			
			#項目処理【＋文書を登録】:document_form.html空。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
