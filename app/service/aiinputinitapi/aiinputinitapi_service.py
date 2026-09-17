#BasicService.vm
#make Service templete
# 傾聴内容変換AI画面初期表示サービス
# 帳票様式（API119）・支援テーマ（API120）・担当者選択肢（API121）・業種（API124）を実データ（DB）から取得する
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from utils.jsonwfc_object import JSONWFCObject
from app.dto.aiinputinitapi.aiinputinitapi_dto import AiinputinitapiDto
from app.dao.api119_getreportforms.api119_getreportforms_dao import Api119GetreportformsDao
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api121_getstaffoptions.api121_getstaffoptions_dao import Api121GetstaffoptionsDao
from app.dao.api124_getindustries.api124_getindustries_dao import Api124GetindustriesDao
from app.dto.api119_getreportforms.api119_getreportforms_dto import Api119GetreportformsDto
from app.dto.api120_getthemes.api120_getthemes_dto import Api120GetthemesDto
from app.dto.api121_getstaffoptions.api121_getstaffoptions_dto import Api121GetstaffoptionsDto
from app.dto.api124_getindustries.api124_getindustries_dto import Api124GetindustriesDto
import utils.string_util
import utils.mysqldb_utils


class AiinputinitapiService :

	#	#
	# 傾聴内容変換AI画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aiinputinitapi(self,aiinputinitapi_dto,jsonObj) :

		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI画面初期表示_AiInputInitAPI_(API)

			#「項目処理」（共通関数:AiInputInitAPI）,パラメータは（）

			#以下の処理を行う。

			#対象年度（fiscal_year_id）を取得する。マスタ「mst_fiscal_year」の最新年度を使用する。
			fiscal_year_id = ""
			fiscalRows = utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQLNoParams(
				"SELECT fiscal_year_id FROM mst_fiscal_year ORDER BY fiscal_year_code DESC, fiscal_year_id DESC LIMIT 1"))
			if fiscalRows :
				fiscal_year_id = str(fiscalRows[0].get("fiscal_year_id") or "")

			#セッションの組織情報（都道府県コード／商工会コード）を取得する。
			prefecture_code = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE") or "")
			shokokai_cd = utils.string_util.changeNullToBlank(session.get("SHOKOKAI_CD") or "")

			#関数「API119_GetReportForms」：帳票様式一覧を取得する（実データ：mst_form）。
			api119_getreportforms = Api119GetreportformsDto.dict_to_json({})
			api119_getreportforms.fiscalyearid = fiscal_year_id
			form_rows = Api119GetreportformsDao().api119_getreportforms(api119_getreportforms) or []

			#関数「API120_GetThemes」：支援テーマ一覧を取得する（実データ：mst_theme）。
			api120_getthemes = Api120GetthemesDto.dict_to_json({})
			api120_getthemes.fiscalyearid = fiscal_year_id
			theme_rows = Api120GetthemesDao().api120_getthemes(api120_getthemes) or []

			#関数「API121_GetStaffOptions」：担当者選択肢一覧を取得する（実データ：mst_user_account）。
			api121_getstaffoptions = Api121GetstaffoptionsDto.dict_to_json({})
			api121_getstaffoptions.prefecturecode = prefecture_code
			api121_getstaffoptions.shokokaicd = shokokai_cd
			staff_rows = Api121GetstaffoptionsDao().api121_getstaffoptions(api121_getstaffoptions) or []

			#関数「API124_GetIndustries」：業種一覧を取得する（実データ：mst_industry）。
			api124_getindustries = Api124GetindustriesDto.dict_to_json({})
			api124_getindustries.fiscalyearid = fiscal_year_id
			industry_rows = Api124GetindustriesDao().api124_getindustries(api124_getindustries) or []

			#取得結果をJSON形式でフロントエンドへ返却する（日付型は文字列化しておく）。
			jsonObj.setHtml("dragForms", json.dumps(form_rows, default=str, ensure_ascii=False))
			jsonObj.setHtml("dragThemes", json.dumps(theme_rows, default=str, ensure_ascii=False))
			jsonObj.setHtml("dragStaff", json.dumps(staff_rows, default=str, ensure_ascii=False))
			jsonObj.setHtml("dragIndustries", json.dumps(industry_rows, default=str, ensure_ascii=False))
			jsonObj.setHtml("dragFiscalYear", fiscal_year_id)
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "画面初期表示データの取得に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
