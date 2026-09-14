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
from app.dto.documentversiondownloadapi.documentversiondownloadapi_dto import DocumentversiondownloadapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DocumentversiondownloadapiService :

	#	# 
	# ナレッジ文書詳細⬇ ダウンロード
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentversiondownloadapi(self,documentversiondownloadapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		ID = documentversiondownloadapi_dto.id#GeninusClientScript 1318
		VERSION = documentversiondownloadapi_dto.version#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書詳細⬇ ダウンロード_DocumentVersionDownloadAPI_(API)
			
			#「項目処理」（共通関数:DocumentVersionDownloadAPI）,パラメータは（id,version）
			
			#以下の処理を行う。
			
			#エクスポート開始。
			
			#画面:ナレッジ文書詳細
			
			#項目:⬇ダウンロード
			
			#エクスポートパス:/XXX/YYY/
			
			#エクスポートファイル名:aaa+<システム日付(yyyyMMddHHmmssSSS)>+<ログインID>+.xlsx
			
			#エクスポート終了。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
