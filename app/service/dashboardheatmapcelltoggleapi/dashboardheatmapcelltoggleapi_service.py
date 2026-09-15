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
from app.dao.api182_dashboardheatmapcelltoggle.api182_dashboardheatmapcelltoggle_dao import Api182DashboardheatmapcelltoggleDao
from app.dto.api182_dashboardheatmapcelltoggle.api182_dashboardheatmapcelltoggle_dto import Api182DashboardheatmapcelltoggleDto
from app.dto.dashboardheatmapcelltoggleapi.dashboardheatmapcelltoggleapi_dto import DashboardheatmapcelltoggleapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DashboardheatmapcelltoggleapiService :

	#	# 
	# ダッシュボード（全国連）ヒートマップセル除外トグル
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def dashboardheatmapcelltoggleapi(self,dashboardheatmapcelltoggleapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		CELL_KEY = dashboardheatmapcelltoggleapi_dto.cellkey#GeninusClientScript 1318
		EXCLUDED = dashboardheatmapcelltoggleapi_dto.excluded#GeninusClientScript 1318
		api182_dashboardheatmapcelltoggle = Api182DashboardheatmapcelltoggleDto.dict_to_json({}) #CommonFunction 110
		api182_dashboardheatmapcelltoggleList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ダッシュボード（全国連）ヒートマップセル除外トグル_DashboardHeatmapCellToggleAPI_(API)
			
			#「項目処理」（共通関数:DashboardHeatmapCellToggleAPI）,パラメータは（cell_key,excluded）
			
			#以下の処理を行う。
			
			#関数「API182_DashboardHeatmapCellToggle」の「db_API182_DashboardHeatmapCellToggle」メソッドを行う,パラメータは「cell_key,excluded」。
			
			# cell_key
			api182_dashboardheatmapcelltoggle.cellkey = CELL_KEY #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# excluded
			api182_dashboardheatmapcelltoggle.excluded = EXCLUDED #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api182_dashboardheatmapcelltoggleList = Api182DashboardheatmapcelltoggleDao().api182_dashboardheatmapcelltoggle(api182_dashboardheatmapcelltoggle)
			api182_dashboardheatmapcelltogglelistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api182_dashboardheatmapcelltoggleList != None :
				api182_dashboardheatmapcelltogglelistVar = api182_dashboardheatmapcelltoggleList.fetchall() if hasattr(api182_dashboardheatmapcelltoggleList, 'fetchall') else api182_dashboardheatmapcelltoggleList
			if api182_dashboardheatmapcelltogglelistVar != None and len(api182_dashboardheatmapcelltogglelistVar) > 0 :
				SHUTOKUKENSUU = str(len(api182_dashboardheatmapcelltogglelistVar))
			#関数「API182_DashboardHeatmapCellToggle」の「db_API182_DashboardHeatmapCellToggle」取得結果をGrid「monthly_stats」に設定。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api182_dashboardheatmapcelltogglelistVar != None and len(api182_dashboardheatmapcelltogglelistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api182_dashboardheatmapcelltogglelistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api182_dashboardheatmapcelltogglelistVar[i]
					selMap ={} #GeniusGrid681
					#GeniusGrid681
					mapList.insert(len(mapList),selMap)
			result = json.dumps(mapList, ensure_ascii=False)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
