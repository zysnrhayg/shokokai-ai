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
from app.dao.api124_insertreport.api124_insertreport_dao import Api124InsertreportDao
from app.dao.api125_insertreporttheme.api125_insertreporttheme_dao import Api125InsertreportthemeDao
from app.dto.api124_insertreport.api124_insertreport_dto import Api124InsertreportDto
from app.dto.api125_insertreporttheme.api125_insertreporttheme_dto import Api125InsertreportthemeDto
from app.dto.formnewsaveapi.formnewsaveapi_dto import FormnewsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class FormnewsaveapiService :

	#	# 
	# 報告書新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formnewsaveapi(self,formnewsaveapi_dto,jsonObj) :
			
		#GeniusClientScript 1315
		FORM_CODE = formnewsaveapi_dto.formcode#GeninusClientScript 1318
		REPORT_DATE = formnewsaveapi_dto.reportdate#GeninusClientScript 1318
		TIME_START = formnewsaveapi_dto.timestart#GeninusClientScript 1318
		TIME_END = formnewsaveapi_dto.timeend#GeninusClientScript 1318
		STAFF_MAIN_CODE = formnewsaveapi_dto.staffmaincode#GeninusClientScript 1318
		STAFF_SUB_CODE = formnewsaveapi_dto.staffsubcode#GeninusClientScript 1318
		THEME_CODES = formnewsaveapi_dto.themecodes#GeninusClientScript 1318
		INDUSTRY = formnewsaveapi_dto.industry#GeninusClientScript 1318
		BUSINESS_NAME = formnewsaveapi_dto.businessname#GeninusClientScript 1318
		BUSINESS_PERSON = formnewsaveapi_dto.businessperson#GeninusClientScript 1318
		CONTENT = formnewsaveapi_dto.content#GeninusClientScript 1318
		SUMMARY = formnewsaveapi_dto.summary#GeninusClientScript 1318
		STATUS = formnewsaveapi_dto.status#GeninusClientScript 1318
		TAIOUBIJI_KAISHI_ = ""
		TAIOUBIJI_SHUURYOU_ = "";
		GYOUSHU = ""
		JIGYOUSHOMEI = ""
		TANTOUSHAMEI = ""
		NAIYOU = ""
		GAIYOU = ""
		NYUURYOKU_CHECK_NG = "" #GeniusVarItem 251
		api124_insertreport = Api124InsertreportDto.dict_to_json({}) #CommonFunction 110
		api125_insertreporttheme = Api125InsertreportthemeDto.dict_to_json({}) #CommonFunction 110
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書新規画面登録ボタン_FormNewSaveAPI_(API)
			
			#「項目処理」（共通関数:FormNewSaveAPI）,パラメータは（form_code,report_date,time_start,time_end,staff_main_code,staff_sub_code,theme_codes,industry,business_name,business_person,content,summary,status）
			
			#以下の処理を行う。
			
			#その他の場合,以下の処理を行う。
			#GeninusClientScript 955 test
			# 判定条件が生成されていないため、入力チェックNGフラグで代替している。設計書に合わせて要見直し。
			if NYUURYOKU_CHECK_NG.replace(" ", "") == "true" : #GeniusContion 823
				pass
			else :
				#<対応日時（開始）>が<対応日時（終了）>以上の場合,以下の処理を行う。
				#GeniusClientScript 983
				if (TAIOUBIJI_KAISHI_.replace(" ", "")>=TAIOUBIJI_SHUURYOU_) : #GeniusContion 823
					#GeniusContion 823
					#処理終了。
					pass
					#GeniusClientScript 1207
				#その他の場合,以下の処理を行う。
				#GeninusClientScript 955 test
				else :
					#<業種>が100より大きい,または<事業所名>が200より大きい,または<担当者名>が100より大きい,または<内容>が20000より大きい,または<概要>が2000より大きい場合,以下の処理を行う。
					#GeniusClientScript 983
					if utils.string_util.changeStringToDouble(GYOUSHU) > 100 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(JIGYOUSHOMEI) > 200 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(TANTOUSHAMEI) > 100 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(NAIYOU) > 20000 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(GAIYOU) > 2000 : #GeniusConditionParam 207 : #GeniusContion 823
						#GeniusConditionParam 207 or utils.string_util.changeStringToDouble(JIGYOUSHOMEI) > 200 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(TANTOUSHAMEI) > 100 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(NAIYOU) > 20000 : #GeniusConditionParam 207 or utils.string_util.changeStringToDouble(GAIYOU) > 2000 : #GeniusConditionParam 207 : #GeniusContion 823
						#処理終了。
						pass
						#GeniusClientScript 1207
					#その他の場合,以下の処理を行う。
					#GeninusClientScript 955 test
					else :
						#関数「API124_InsertReport」の「db_API124_InsertReport」メソッドを行う,パラメータは「report_code,form_code,fiscal_year_id,prefecture_code,shokokai_cd,theme_id,industry,report_date,summary,content,time_start,time_end,business_person,business_name,staff_main_name,staff_sub_name,status」。
						
						# report_code
						api124_insertreport.reportcode = REPORT_CODE #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# form_code
						api124_insertreport.formcode = FORM_CODE #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# fiscal_year_id
						api124_insertreport.fiscalyearid = FISCAL_YEAR_ID #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# prefecture_code
						api124_insertreport.prefecturecode = PREFECTURE_CODE #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# shokokai_cd
						api124_insertreport.shokokaicd = SHOKOKAI_CD #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# theme_id
						api124_insertreport.themeid = THEME_ID #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# industry
						api124_insertreport.industry = INDUSTRY #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# report_date
						api124_insertreport.reportdate = REPORT_DATE #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# summary
						api124_insertreport.summary = SUMMARY #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# content
						api124_insertreport.content = CONTENT #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# time_start
						api124_insertreport.timestart = TIME_START #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# time_end
						api124_insertreport.timeend = TIME_END #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# business_person
						api124_insertreport.businessperson = BUSINESS_PERSON #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# business_name
						api124_insertreport.businessname = BUSINESS_NAME #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# staff_main_name
						api124_insertreport.staffmainname = STAFF_MAIN_NAME #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# staff_sub_name
						api124_insertreport.staffsubname = STAFF_SUB_NAME #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# status
						api124_insertreport.status = STATUS #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						Api124InsertreportDao().api124_insertreport(api124_insertreport) #ResultGenerator 104
						#ResultGenerator 104
						#関数「API125_InsertReportTheme」の「db_API125_InsertReportTheme」メソッドを行う,パラメータは「report_id,theme_id」。
						
						# report_id
						api125_insertreporttheme.reportid = REPORT_ID #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						# theme_id
						api125_insertreporttheme.themeid = THEME_ID #ArgumentGenerator 274
						#ArgumentGenerator 274
						
						Api125InsertreportthemeDao().api125_insertreporttheme(api125_insertreporttheme) #ResultGenerator 104
						#ResultGenerator 104
						#処理終了。
						pass
						#GeniusClientScript 1207
					#処理終了。
					#GeniusClientScript 1207
				#処理終了。
				#GeniusClientScript 1207
			#処理終了。
			
		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end") 
		
			
	
	
