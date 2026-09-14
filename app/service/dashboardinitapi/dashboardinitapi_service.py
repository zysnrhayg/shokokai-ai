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
from app.dao.api112_getdashboardkpi.api112_getdashboardkpi_dao import Api112GetdashboardkpiDao
from app.dao.api113_getkpithemebreakdown.api113_getkpithemebreakdown_dao import Api113GetkpithemebreakdownDao
from app.dao.api114_getheatmapprefecture.api114_getheatmapprefecture_dao import Api114GetheatmapprefectureDao
from app.dao.api116_getrecentreports.api116_getrecentreports_dao import Api116GetrecentreportsDao
from app.dao.api117_getnotices.api117_getnotices_dao import Api117GetnoticesDao
from app.dto.api112_getdashboardkpi.api112_getdashboardkpi_dto import Api112GetdashboardkpiDto
from app.dto.api113_getkpithemebreakdown.api113_getkpithemebreakdown_dto import Api113GetkpithemebreakdownDto
from app.dto.api114_getheatmapprefecture.api114_getheatmapprefecture_dto import Api114GetheatmapprefectureDto
from app.dto.api116_getrecentreports.api116_getrecentreports_dto import Api116GetrecentreportsDto
from app.dto.api117_getnotices.api117_getnotices_dto import Api117GetnoticesDto
from app.dto.dashboardinitapi.dashboardinitapi_dto import DashboardinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class DashboardinitapiService :

	#	# 
	# ダッシュボード（商工会）ダッシュボードを開く（初期データ取
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def dashboardinitapi(self,dashboardinitapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		ROLE_CODE = dashboardinitapi_dto.rolecode#GeninusClientScript 1318
		api112_getdashboardkpi = Api112GetdashboardkpiDto.dict_to_json({}) #CommonFunction 110
		api112_getdashboardkpiList = None #ResultGenerator 72
		#ResultGenerator 80
		SHUTOKUKENSUU = ""
		#_dto api112_getdashboardkpi_dto = None #ResultGenerator 119
		#ResultGenerator365
		FISCALYEARID = ""
		SUPPORTCOUNT = ""
		AIACTIVITYCOUNT = ""
		api113_getkpithemebreakdown = Api113GetkpithemebreakdownDto.dict_to_json({}) #CommonFunction 110
		api113_getkpithemebreakdownList = None #ResultGenerator 72
		#_dto api113_getkpithemebreakdown_dto = None #ResultGenerator 119
		THEMECODE = ""
		LABEL = ""
		BADGECLASS = ""
		api114_getheatmapprefecture = Api114GetheatmapprefectureDto.dict_to_json({}) #CommonFunction 110
		api114_getheatmapprefectureList = None #ResultGenerator 72
		#_dto api114_getheatmapprefecture_dto = None #ResultGenerator 119
		PREFECTURECODE = ""
		NAME = ""
		YEARTODATECOUNT = ""
		api117_getnotices = Api117GetnoticesDto.dict_to_json({}) #CommonFunction 110
		api117_getnoticesList = None #ResultGenerator 72
		#_dto api117_getnotices_dto = None #ResultGenerator 119
		CONTENT = ""
		api116_getrecentreports = Api116GetrecentreportsDto.dict_to_json({}) #CommonFunction 110
		api116_getrecentreportsList = None #ResultGenerator 72
		#_dto api116_getrecentreports_dto = None #ResultGenerator 119
		REPORTID = ""
		REPORTDATE = ""
		THEMELABEL = ""
		FORMLABEL = ""
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ダッシュボード（商工会）ダッシュボードを開く（初期データ取得）_DashboardInitAPI_(API)
			
			#「項目処理」（共通関数:DashboardInitAPI）,パラメータは（role_code）
			
			#以下の処理を行う。
			
			#関数「API112_GetDashboardKpi」の「db_API112_GetDashboardKpi」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<fiscal_year_id>=fiscal_year_id,<support_count>=support_count,<ai_activity_count>=ai_activity_count」を設定する。
			
			# prefecture_code
			api112_getdashboardkpi.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api112_getdashboardkpi.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api112_getdashboardkpiList = Api112GetdashboardkpiDao().api112_getdashboardkpi(api112_getdashboardkpi)
			api112_getdashboardkpilistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api112_getdashboardkpiList != None :
				api112_getdashboardkpilistVar = api112_getdashboardkpiList.fetchall() if hasattr(api112_getdashboardkpiList, 'fetchall') else api112_getdashboardkpiList
			if api112_getdashboardkpilistVar != None and len(api112_getdashboardkpilistVar) > 0 :
				SHUTOKUKENSUU = str(len(api112_getdashboardkpilistVar))
			# --LINE114 retrieved first value
			if api112_getdashboardkpilistVar != None and len(api112_getdashboardkpilistVar) > 0 :
				rec = api112_getdashboardkpilistVar[0]
				FISCALYEARID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "fiscal_year_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUPPORTCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "support_count")) # ResultGenerator 385
				# ResultGenerator 385
				
				AIACTIVITYCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "ai_activity_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API113_GetKpiThemeBreakdown」の「db_API113_GetKpiThemeBreakdown」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<fiscal_year_id>=fiscal_year_id,<theme_code>=theme_code,<label>=label,<badge_class>=badge_class,<support_count>=support_count」を設定する。
			
			# prefecture_code
			api113_getkpithemebreakdown.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api113_getkpithemebreakdown.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api113_getkpithemebreakdownList = Api113GetkpithemebreakdownDao().api113_getkpithemebreakdown(api113_getkpithemebreakdown)
			api113_getkpithemebreakdownlistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api113_getkpithemebreakdownList != None :
				api113_getkpithemebreakdownlistVar = api113_getkpithemebreakdownList.fetchall() if hasattr(api113_getkpithemebreakdownList, 'fetchall') else api113_getkpithemebreakdownList
			if api113_getkpithemebreakdownlistVar != None and len(api113_getkpithemebreakdownlistVar) > 0 :
				SHUTOKUKENSUU = str(len(api113_getkpithemebreakdownlistVar))
			# --LINE114 retrieved first value
			if api113_getkpithemebreakdownlistVar != None and len(api113_getkpithemebreakdownlistVar) > 0 :
				rec = api113_getkpithemebreakdownlistVar[0]
				FISCALYEARID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "fiscal_year_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				LABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")) # ResultGenerator 385
				# ResultGenerator 385
				
				BADGECLASS = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "badge_class")) # ResultGenerator 385
				# ResultGenerator 385
				
				SUPPORTCOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "support_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API114_GetHeatmapPrefecture」の「db_API114_GetHeatmapPrefecture」メソッドを行う,パラメータは「prefecture_code,fiscal_year_id」,戻り値設定は「<prefecture_code>=prefecture_code,<name>=name,<year_to_date_count>=year_to_date_count」を設定する。
			
			# prefecture_code
			api114_getheatmapprefecture.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# fiscal_year_id
			api114_getheatmapprefecture.fiscalyearid = FISCALYEARID #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api114_getheatmapprefectureList = Api114GetheatmapprefectureDao().api114_getheatmapprefecture(api114_getheatmapprefecture)
			api114_getheatmapprefecturelistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api114_getheatmapprefectureList != None :
				api114_getheatmapprefecturelistVar = api114_getheatmapprefectureList.fetchall() if hasattr(api114_getheatmapprefectureList, 'fetchall') else api114_getheatmapprefectureList
			if api114_getheatmapprefecturelistVar != None and len(api114_getheatmapprefecturelistVar) > 0 :
				SHUTOKUKENSUU = str(len(api114_getheatmapprefecturelistVar))
			# --LINE114 retrieved first value
			if api114_getheatmapprefecturelistVar != None and len(api114_getheatmapprefecturelistVar) > 0 :
				rec = api114_getheatmapprefecturelistVar[0]
				PREFECTURECODE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code")) # ResultGenerator 385
				# ResultGenerator 385
				
				NAME = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "name")) # ResultGenerator 385
				# ResultGenerator 385
				
				YEARTODATECOUNT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "year_to_date_count")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API117_GetNotices」の「db_API117_GetNotices」メソッドを行う,パラメータは「role_code」,戻り値設定は「<content>=content」を設定する。
			
			# role_code
			api117_getnotices.rolecode = ROLE_CODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api117_getnoticesList = Api117GetnoticesDao().api117_getnotices(api117_getnotices)
			api117_getnoticeslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api117_getnoticesList != None :
				api117_getnoticeslistVar = api117_getnoticesList.fetchall() if hasattr(api117_getnoticesList, 'fetchall') else api117_getnoticesList
			if api117_getnoticeslistVar != None and len(api117_getnoticeslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api117_getnoticeslistVar))
			# --LINE114 retrieved first value
			if api117_getnoticeslistVar != None and len(api117_getnoticeslistVar) > 0 :
				rec = api117_getnoticeslistVar[0]
				CONTENT = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content")) # ResultGenerator 385
				# ResultGenerator 385
				
			#関数「API116_GetRecentReports」の「db_API116_GetRecentReports」メソッドを行う,パラメータは「prefecture_code,shokokai_cd」,戻り値設定は「<report_id>=report_id,<report_date>=report_date,<theme_label>=theme_label,<form_label>=form_label」を設定する。
			
			# prefecture_code
			api116_getrecentreports.prefecturecode = PREFECTURECODE #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			# shokokai_cd
			api116_getrecentreports.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
			#ArgumentGenerator 274
			
			#ReulstGenerator 87
			api116_getrecentreportsList = Api116GetrecentreportsDao().api116_getrecentreports(api116_getrecentreports)
			api116_getrecentreportslistVar = None #ResultGenerator 89
			#ResultGenerator 89
			if api116_getrecentreportsList != None :
				api116_getrecentreportslistVar = api116_getrecentreportsList.fetchall() if hasattr(api116_getrecentreportsList, 'fetchall') else api116_getrecentreportsList
			if api116_getrecentreportslistVar != None and len(api116_getrecentreportslistVar) > 0 :
				SHUTOKUKENSUU = str(len(api116_getrecentreportslistVar))
			# --LINE114 retrieved first value
			if api116_getrecentreportslistVar != None and len(api116_getrecentreportslistVar) > 0 :
				rec = api116_getrecentreportslistVar[0]
				REPORTID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_id")) # ResultGenerator 385
				# ResultGenerator 385
				
				REPORTDATE = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "report_date")) # ResultGenerator 385
				# ResultGenerator 385
				
				THEMELABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_label")) # ResultGenerator 385
				# ResultGenerator 385
				
				FORMLABEL = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_label")) # ResultGenerator 385
				# ResultGenerator 385
				
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
