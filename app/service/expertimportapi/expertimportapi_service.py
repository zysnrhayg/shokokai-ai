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
from app.dto.expertimportapi.expertimportapi_dto import ExpertimportapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class ExpertimportapiService :

	#	# 
	# 専門家派遣報告取込取り込む
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def expertimportapi(self,expertimportapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		FILE_NAME = expertimportapi_dto.filename #ファイル名のみ。中身未解析 #GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#専門家派遣報告取込取り込む_ExpertImportAPI_(API)
			
			#「項目処理」（共通関数:ExpertImportAPI）,パラメータは（file_name（ファイル名のみ。中身未解析））
			
			#以下の処理を行う。
			
			#処理終了。
			
			pass
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
