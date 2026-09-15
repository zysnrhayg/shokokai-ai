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
from app.dao.api184_dashboardheatmappage.api184_dashboardheatmappage_dao import Api184DashboardheatmappageDao
from app.dto.api184_dashboardheatmappage.api184_dashboardheatmappage_dto import Api184DashboardheatmappageDto
from app.dto.dashboardheatmappageapi.dashboardheatmappageapi_dto import DashboardheatmappageapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DashboardheatmappageapiService :

	#	# 
	# ダッシュボード（全国連）ヒートマップページ送り
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def dashboardheatmappageapi(self,dashboardheatmappageapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		PAGE = dashboardheatmappageapi_dto.page#GeninusClientScript 1318
		PAGE_SIZE = dashboardheatmappageapi_dto.pagesize#GeninusClientScript 1318
		ROLE_CODE = dashboardheatmappageapi_dto.rolecode#GeninusClientScript 1318
		FISCAL_YEAR_CODE = dashboardheatmappageapi_dto.fiscalyearcode#GeninusClientScript 1318
		EXCLUDED_KEYS = dashboardheatmappageapi_dto.excludedkeys#GeninusClientScript 1318
		api184_dashboardheatmappage = Api184DashboardheatmappageDto.dict_to_json({}) #CommonFunction 110
		api184_dashboardheatmappageList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ダッシュボード（全国連）ヒートマップページ送り_DashboardHeatmapPageAPI_(API)
			
			#「項目処理」（共通関数:DashboardHeatmapPageAPI）,パラメータは（page,page_size,role_code,fiscal_year_code,excluded_keys）
			
			#以下の処理を行う。
			
			#関数「API184_DashboardHeatmapPage」の「db_API184_DashboardHeatmapPage」メソッドを行う,パラメータは「page,page_size,role_code,fiscal_year_code,excluded_keys」。
			
			# page
			api184_dashboardheatmappage.page = PAGE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# page_size
			api184_dashboardheatmappage.pagesize = PAGE_SIZE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# role_code
			api184_dashboardheatmappage.rolecode = ROLE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fiscal_year_code
			api184_dashboardheatmappage.fiscalyearcode = FISCAL_YEAR_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# excluded_keys
			api184_dashboardheatmappage.excludedkeys = EXCLUDED_KEYS #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api184_dashboardheatmappageList = Api184DashboardheatmappageDao().api184_dashboardheatmappage(api184_dashboardheatmappage)
			api184_dashboardheatmappagelistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api184_dashboardheatmappageList != None :
				api184_dashboardheatmappagelistVar = api184_dashboardheatmappageList.fetchall() if hasattr(api184_dashboardheatmappageList, 'fetchall') else api184_dashboardheatmappageList
			if api184_dashboardheatmappagelistVar != None and len(api184_dashboardheatmappagelistVar) > 0 :
				SHUTOKUKENSUU = str(len(api184_dashboardheatmappagelistVar))
			#関数「API184_DashboardHeatmapPage」の「db_API184_DashboardHeatmapPage」取得結果をGrid「cells」に設定。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api184_dashboardheatmappagelistVar != None and len(api184_dashboardheatmappagelistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api184_dashboardheatmappagelistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api184_dashboardheatmappagelistVar[i]
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
		
			
	
	
