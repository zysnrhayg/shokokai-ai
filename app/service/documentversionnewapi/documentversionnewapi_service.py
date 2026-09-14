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
from app.dto.documentversionnewapi.documentversionnewapi_dto import DocumentversionnewapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DocumentversionnewapiService :

	#	# 
	# ナレッジ文書詳細画面版登録
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentversionnewapi(self,documentversionnewapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		KNOWLEDGE_DOCUMENT_ID = documentversionnewapi_dto.knowledgedocumentid#GeninusClientScript 1318
		FILE = documentversionnewapi_dto.file#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書詳細画面版登録_DocumentVersionNewAPI_(API)
			
			#「項目処理」（共通関数:DocumentVersionNewAPI）,パラメータは（knowledge_document_id,file）
			
			#以下の処理を行う。
			
			#バックアップパス:/XXX/YYY/BBB/。
			
			#インポート開始。
			
			#画面:ナレッジ文書詳細画面
			
			#項目:＋新しい版をアップロード
			
			#インポートパス:/XXX/YYY/
			
			#インポートファイル名:importFile.txt
			
			#バックアップパス:/XXX/YYY/BBB/
			
			#インポート終了。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
