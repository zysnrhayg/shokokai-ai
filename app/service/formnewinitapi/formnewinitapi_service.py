#BasicService.vm
#make Service templete
# 報告書新規画面初期表示サービス
# 帳票様式・支援テーマ・担当者をDBから取得し、フロントエンドへ返却する
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
from app.dao.api119_getreportforms.api119_getreportforms_dao import Api119GetreportformsDao
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api121_getstaffoptions.api121_getstaffoptions_dao import Api121GetstaffoptionsDao
from app.dto.api119_getreportforms.api119_getreportforms_dto import Api119GetreportformsDto
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api121_getstaffoptions.api121_getstaffoptions_dto import Api121GetstaffoptionsDto
from app.dto.formnewinitapi.formnewinitapi_dto import FormnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util


class FormnewinitapiService :

	#
	# 報告書新規画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formnewinitapi(self,formnewinitapi_dto,jsonObj) :

		#GeniusClientScript 1315
		PREFILL = formnewinitapi_dto.prefill#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書新規画面初期表示_FormNewInitAPI_(API)

			#「項目処理」（共通関数:FormNewInitAPI）,パラメータは（prefill）

			#以下の処理を行う。

			#セッションから年度ID・都道府県コード・商工会コードを取得する
			FISCAL_YEAR_ID = utils.string_util.changeNullToBlank(str(session.get("FISCAL_YEAR_ID") or ""))
			PREFECTURE_CODE = utils.string_util.changeNullToBlank(str(session.get("PREFECTURE_CODE") or ""))
			SHOKOKAI_CD = utils.string_util.changeNullToBlank(str(session.get("SHOKOKAI_CD") or ""))

			#関数「API119_GetReportForms」：帳票様式一覧を取得する
			api119_getreportforms = Api119GetreportformsDto.dict_to_json({})
			api119_getreportforms.fiscalyearid = FISCAL_YEAR_ID
			api119_getreportformsList = Api119GetreportformsDao().api119_getreportforms(api119_getreportforms)
			api119_getreportformslistVar = None
			if api119_getreportformsList != None :
				api119_getreportformslistVar = api119_getreportformsList.fetchall() if hasattr(api119_getreportformsList, 'fetchall') else api119_getreportformsList

			#帳票様式一覧をJSON配列に変換する
			forms_array = []
			if api119_getreportformslistVar != None :
				for rec in api119_getreportformslistVar :
					forms_array.append({
						"form_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "form_code")),
						"full_label": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "full_label")),
						"short_label": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "short_label")),
					})

			#関数「API120_GetThemes」：支援テーマ一覧を取得する
			api120_getthemes = Api120GetthemesDto.dict_to_json({})
			api120_getthemes.fiscalyearid = FISCAL_YEAR_ID
			api120_getthemesList = Api120GetthemesDao().api120_getthemes(api120_getthemes)
			api120_getthemeslistVar = None
			if api120_getthemesList != None :
				api120_getthemeslistVar = api120_getthemesList.fetchall() if hasattr(api120_getthemesList, 'fetchall') else api120_getthemesList

			#支援テーマ一覧をJSON配列に変換する
			themes_array = []
			if api120_getthemeslistVar != None :
				for rec in api120_getthemeslistVar :
					themes_array.append({
						"theme_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")),
						"theme_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")),
						"label": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")),
						"filter_group": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "filter_group")),
					})

			#関数「API121_GetStaffOptions」：担当者一覧を取得する
			api121_getstaffoptions = Api121GetstaffoptionsDto.dict_to_json({})
			api121_getstaffoptions.prefecturecode = PREFECTURE_CODE
			api121_getstaffoptions.shokokaicd = SHOKOKAI_CD
			api121_getstaffoptionsList = Api121GetstaffoptionsDao().api121_getstaffoptions(api121_getstaffoptions)
			api121_getstaffoptionslistVar = None
			if api121_getstaffoptionsList != None :
				api121_getstaffoptionslistVar = api121_getstaffoptionsList.fetchall() if hasattr(api121_getstaffoptionsList, 'fetchall') else api121_getstaffoptionsList

			#担当者一覧をJSON配列に変換する
			staff_array = []
			if api121_getstaffoptionslistVar != None :
				for rec in api121_getstaffoptionslistVar :
					staff_array.append({
						"user_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "user_id")),
						"shokuin_kj": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "shokuin_kj")),
					})

			#取得結果をフロントエンドへ返却する
			jsonObj.setValue("dragForms", forms_array)
			jsonObj.setValue("dragThemes", themes_array)
			jsonObj.setValue("dragStaff", staff_array)
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "初期データの取得が完了しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "初期データの取得に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
