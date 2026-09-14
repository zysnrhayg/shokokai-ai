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
from app.dto.scr_110_30.scr_110_30_dto import Scr11030Dto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class Scr11030initService :

	#	# 
	# ページの初期化
	# @param scr_110_30Entity
	# @return json data
	# @throws Exception
	#
	def sscr_110_30init(self,scr_110_30_dto) :
			
		
		
		#UltimateGeniusBean 617
		mode = None
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#PageInitBuild 140行
			jsonObj = JSONWFCObject()
			#GridSearchBuildFormt 297
			mode = utils.string_util.changeNullToBlank(utils.string_util.escapeSQLTags(utils.string_util.changeNullToBlank(scr_110_30_dto.mode)))
			jsonObj.setValue("mode",mode)
			return jsonObj
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
