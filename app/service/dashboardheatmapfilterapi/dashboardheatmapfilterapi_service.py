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
from app.dao.api180_dashboardheatmapfilter.api180_dashboardheatmapfilter_dao import Api180DashboardheatmapfilterDao
from app.dto.api180_dashboardheatmapfilter.api180_dashboardheatmapfilter_dto import Api180DashboardheatmapfilterDto
from app.dto.dashboardheatmapfilterapi.dashboardheatmapfilterapi_dto import DashboardheatmapfilterapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DashboardheatmapfilterapiService :

	#	# 
	# ダッシュボード（全国連）ヒートマップ絞込（地方／グループ）
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def dashboardheatmapfilterapi(self,dashboardheatmapfilterapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		GROUP_VALUES = dashboardheatmapfilterapi_dto.groupvalues#GeninusClientScript 1318
		INCLUDE_ALL = dashboardheatmapfilterapi_dto.includeall#GeninusClientScript 1318
		api180_dashboardheatmapfilter = Api180DashboardheatmapfilterDto.dict_to_json({}) #CommonFunction 110
		api180_dashboardheatmapfilterList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ダッシュボード（全国連）ヒートマップ絞込（地方／グループ）_DashboardHeatmapFilterAPI_(API)
			
			#「項目処理」（共通関数:DashboardHeatmapFilterAPI）,パラメータは（group_values,include_all）
			
			#以下の処理を行う。
			
			#関数「API180_DashboardHeatmapFilter」の「db_API180_DashboardHeatmapFilter」メソッドを行う,パラメータは「group_values,include_all」。
			
			# group_values
			api180_dashboardheatmapfilter.groupvalues = GROUP_VALUES #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# include_all
			api180_dashboardheatmapfilter.includeall = INCLUDE_ALL #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api180_dashboardheatmapfilterList = Api180DashboardheatmapfilterDao().api180_dashboardheatmapfilter(api180_dashboardheatmapfilter)
			api180_dashboardheatmapfilterlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api180_dashboardheatmapfilterList != None :
				api180_dashboardheatmapfilterlistVar = api180_dashboardheatmapfilterList.fetchall() if hasattr(api180_dashboardheatmapfilterList, 'fetchall') else api180_dashboardheatmapfilterList
			if api180_dashboardheatmapfilterlistVar != None and len(api180_dashboardheatmapfilterlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api180_dashboardheatmapfilterlistVar))
			#関数「API180_DashboardHeatmapFilter」の「db_API180_DashboardHeatmapFilter」取得結果をGrid「rows」に設定,20行改ページ。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			if api180_dashboardheatmapfilterlistVar != None and len(api180_dashboardheatmapfilterlistVar) > 0 :#GeniusGrid 647
				#GeniusGrid 647
				for i in range(0, len(api180_dashboardheatmapfilterlistVar)): #GeniusGrid 652
				#GeniusGrid 652
					entity = api180_dashboardheatmapfilterlistVar[i]
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
		
			
	
	
