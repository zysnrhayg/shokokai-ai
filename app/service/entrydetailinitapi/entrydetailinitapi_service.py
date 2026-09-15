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
from app.dao.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_dao import Api143GetknowledgeentrydetailDao
from app.dao.api147_getentrythemes.api147_getentrythemes_dao import Api147GetentrythemesDao
from app.dto.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_dto import Api143GetknowledgeentrydetailDto
from app.dto.api147_getentrythemes.api147_getentrythemes_dto import Api147GetentrythemesDto
from app.dto.entrydetailinitapi.entrydetailinitapi_dto import EntrydetailinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntrydetailinitapiService :

	#
	# 知識データ詳細画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entrydetailinitapi(self,entrydetailinitapi_dto,jsonObj) :

		#GeniusClientScript 1315
		# 詳細表示対象の知識データID（row配下から取得する）
		KNOWLEDGE_ENTRY_ID = entrydetailinitapi_dto.knowledgeentryid#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ詳細画面初期表示_EntryDetailInitAPI_(API)

			#「項目処理」（共通関数:EntryDetailInitAPI）,パラメータは（knowledge_entry_id）

			#知識データIDが空の場合は検索せずに終了する
			if KNOWLEDGE_ENTRY_ID == "" or KNOWLEDGE_ENTRY_ID is None :
				utils.config.global_log.warning("EntryDetailInitAPI: knowledgeentryidが未指定のため検索をスキップします")
				return

			#関数「API143_GetKnowledgeEntryDetail」の「db_API143_GetKnowledgeEntryDetail」メソッドを行う,知識データ詳細を取得する。
			api143_getknowledgeentrydetail = Api143GetknowledgeentrydetailDto.dict_to_json({}) #CommonFunction 110
			api143_getknowledgeentrydetail.knowledgeentryid = KNOWLEDGE_ENTRY_ID #ArgumentGenerator 274
			api143_getknowledgeentrydetailList = Api143GetknowledgeentrydetailDao().api143_getknowledgeentrydetail(api143_getknowledgeentrydetail)

			#詳細情報を格納する辞書を生成する
			entryDetail = {}
			api143_getknowledgeentrydetaillistVar = api143_getknowledgeentrydetailList if api143_getknowledgeentrydetailList != None else []
			if len(api143_getknowledgeentrydetaillistVar) > 0 :
				rec = api143_getknowledgeentrydetaillistVar[0]
				# 知識データID
				entryDetail["knowledge_entry_id"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_entry_id"))
				# ナレッジコード
				entryDetail["knowledge_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_code"))
				# タイトル
				entryDetail["title"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title"))
				# 適用範囲（県コード・県名）
				entryDetail["prefecture_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code"))
				entryDetail["prefecture_name"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_name"))
				# 紐付ファイル（原本文書）
				entryDetail["knowledge_document_id"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id"))
				entryDetail["document_title"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "document_title"))
				# 更新日
				entryDetail["updated_date"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "updated_date"))
				# ステータス
				entryDetail["status"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status"))
				# 本文
				entryDetail["content"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content"))

			#関数「API147_GetEntryThemes」の「db_API147_GetEntryThemes」メソッドを行う,知識データに紐付くテーマ一覧を取得する。
			api147_getentrythemes = Api147GetentrythemesDto.dict_to_json({}) #CommonFunction 110
			api147_getentrythemes.knowledgeentryid = entryDetail.get("knowledge_entry_id", "") if entryDetail else KNOWLEDGE_ENTRY_ID #ArgumentGenerator 274
			api147_getentrythemesList = Api147GetentrythemesDao().api147_getentrythemes(api147_getentrythemes)
			api147_getentrythemeslistVar = api147_getentrythemesList if api147_getentrythemesList != None else []

			#テーマ一覧をバッジ表示用の配列に変換する
			themeList = []
			for i in range(0, len(api147_getentrythemeslistVar)):
				rec = api147_getentrythemeslistVar[i]
				themeList.append({
					"theme_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")),
					"theme_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_code")),
					"label": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "label")),
					"badge_class": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "badge_class"))
				})
			entryDetail["theme_badges"] = themeList

			#日付型などJSON非対応オブジェクトはdefault=strで文字列化して返却する
			result = json.dumps(entryDetail, default=str, ensure_ascii=False)
			jsonObj.setHtml("entryDetail", result)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
