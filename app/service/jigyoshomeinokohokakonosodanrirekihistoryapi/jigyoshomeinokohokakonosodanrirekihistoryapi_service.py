#BasicService.vm
#make Service templete
# 事業所過去相談履歴サービス
# 指定された事業所（business_name）の過去の相談履歴をDB（trn_report等）から取得して返却する
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from utils.jsonwfc_object import JSONWFCObject
from app.dao.api_jigyoshomeinokohokakonosodanrirekihistory.api_jigyoshomeinokohokakonosodanrirekihistory_dao import ApiJigyoshomeinokohokakonosodanrirekihistoryDao
from app.dto.api_jigyoshomeinokohokakonosodanrirekihistory.api_jigyoshomeinokohokakonosodanrirekihistory_dto import ApiJigyoshomeinokohokakonosodanrirekihistoryDto
from app.dto.jigyoshomeinokohokakonosodanrirekihistoryapi.jigyoshomeinokohokakonosodanrirekihistoryapi_dto import JigyoshomeinokohokakonosodanrirekihistoryapiDto
import utils.string_util




class JigyoshomeinokohokakonosodanrirekihistoryapiService :

	#	#
	# 事業所過去相談履歴
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def jigyoshomeinokohokakonosodanrirekihistoryapi(self,jigyoshomeinokohokakonosodanrirekihistoryapi_dto,jsonObj) :

		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#事業所過去相談履歴_JigyoshomeiNoKohoKakoNoSodanRirekiHistoryAPI_(API)

			#「項目処理」（共通関数:JigyoshomeiNoKohoKakoNoSodanRirekiHistoryAPI）,パラメータは（business_name）

			#以下の処理を行う。

			#事業所名が未指定の場合は組織の最新履歴を返すため、空文字は条件から除外する。

			#セッションの組織情報（都道府県コード／商工会コード）を取得する（DTO未指定時のフォールバック）。
			prefecture_code = utils.string_util.changeNullToBlank(
				getattr(jigyoshomeinokohokakonosodanrirekihistoryapi_dto, 'trnreportprefecturecode', '')
				or session.get("PREFECTURE_CODE") or "")
			shokokai_cd = utils.string_util.changeNullToBlank(
				getattr(jigyoshomeinokohokakonosodanrirekihistoryapi_dto, 'trnreportshokokaicd', '')
				or session.get("SHOKOKAI_CD") or "")
			business_name = utils.string_util.changeNullToBlank(
				getattr(jigyoshomeinokohokakonosodanrirekihistoryapi_dto, 'trnreportbusinessname', ''))
			limit = utils.string_util.changeNullToBlank(
				getattr(jigyoshomeinokohokakonosodanrirekihistoryapi_dto, 'limit', '')) or "20"

			#関数「API_JigyoshomeiNoKohoKakoNoSodanRirekiHistory」：過去の相談履歴を取得する（実データ：trn_report＋mst_form＋trn_report_theme＋mst_theme）。
			api_jigyoshomeinokohokakonosodanrirekihistory = ApiJigyoshomeinokohokakonosodanrirekihistoryDto.dict_to_json({})
			api_jigyoshomeinokohokakonosodanrirekihistory.trnreportprefecturecode = prefecture_code
			api_jigyoshomeinokohokakonosodanrirekihistory.trnreportshokokaicd = shokokai_cd
			api_jigyoshomeinokohokakonosodanrirekihistory.trnreportbusinessname = business_name
			api_jigyoshomeinokohokakonosodanrirekihistory.limit = limit
			history_list = ApiJigyoshomeinokohokakonosodanrirekihistoryDao().api_jigyoshomeinokohokakonosodanrirekihistory(api_jigyoshomeinokohokakonosodanrirekihistory) or []

			#関数「API_JigyoshomeiNoKohoKakoNoSodanRirekiHistory」取得結果をJSON形式でGrid「rows」に設定する。
			mapList = [] #GeniusGrid 606
			#GeniusGrid 606
			for entity in history_list :#GeniusGrid 652
			#GeniusGrid 652
				selMap ={} #GeniusGrid681
				#GeniusGrid681
				#取得行の各項目を実データとして設定する（日付型は文字列化しておく）。
				selMap["report_id"] = str(entity.get("report_id") or "")
				selMap["report_date"] = str(entity.get("report_date") or "")
				selMap["summary"] = entity.get("summary") or ""
				selMap["form_short_label"] = entity.get("form_short_label") or ""
				selMap["form_badge_class"] = entity.get("form_badge_class") or ""
				selMap["theme_label"] = entity.get("theme_label") or ""
				mapList.insert(len(mapList),selMap)
			result = json.dumps(mapList, ensure_ascii=False)
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#GeniusGrid748
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "過去の相談履歴の取得に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
