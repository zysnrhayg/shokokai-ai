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
from app.dao.api175_entryforminit.api175_entryforminit_dao import Api175EntryforminitDao
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dto.api143_getknowledgeentrydetail.api143_getknowledgeentrydetail_dto import Api143GetknowledgeentrydetailDto
from app.dto.api147_getentrythemes.api147_getentrythemes_dto import Api147GetentrythemesDto
from app.dto.api175_entryforminit.api175_entryforminit_dto import Api175EntryforminitDto
from app.dto.entryforminitapi.entryforminitapi_dto import EntryforminitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntryforminitapiService :

	#
	# 知識データ編集編集
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entryforminitapi(self,entryforminitapi_dto,jsonObj) :

		#GeniusClientScript 1315
		# 編集対象の知識データID（row配下から取得する）
		ID = entryforminitapi_dto.id#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ編集編集_EntryFormInitAPI_(API)

			#「項目処理」（共通関数:EntryFormInitAPI）,パラメータは（id）

			#知識データIDが空の場合は処理しない
			if ID == "" or ID is None :
				utils.config.global_log.warning("EntryFormInitAPI: idが未指定のため処理をスキップします")
				return

			#関数「API143_GetKnowledgeEntryDetail」の「db_API143_GetKnowledgeEntryDetail」メソッドを行う,編集対象の知識データ詳細を取得する。
			api143_getknowledgeentrydetail = Api143GetknowledgeentrydetailDto.dict_to_json({}) #CommonFunction 110
			api143_getknowledgeentrydetail.knowledgeentryid = ID #ArgumentGenerator 274
			api143_getknowledgeentrydetailList = Api143GetknowledgeentrydetailDao().api143_getknowledgeentrydetail(api143_getknowledgeentrydetail)
			api143_getknowledgeentrydetaillistVar = api143_getknowledgeentrydetailList if api143_getknowledgeentrydetailList != None else []

			#編集フォーム初期値を格納する辞書を生成する
			entryForm = {}
			KNOWLEDGEENTRYID = ""
			if len(api143_getknowledgeentrydetaillistVar) > 0 :
				rec = api143_getknowledgeentrydetaillistVar[0]
				KNOWLEDGEENTRYID = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_entry_id"))
				# 知識データID
				entryForm["knowledge_entry_id"] = KNOWLEDGEENTRYID
				# ナレッジコード
				entryForm["knowledge_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_code"))
				# タイトル
				entryForm["title"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title"))
				# 適用範囲（県コード）
				entryForm["prefecture_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "prefecture_code"))
				# 紐付ファイル（原本文書ID）
				entryForm["knowledge_document_id"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id"))
				# ステータス
				entryForm["status"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "status"))
				# 本文
				entryForm["content"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "content"))

			#関数「API147_GetEntryThemes」の「db_API147_GetEntryThemes」メソッドを行う,選択済みテーマID一覧を取得する。
			api147_getentrythemes = Api147GetentrythemesDto.dict_to_json({}) #CommonFunction 110
			api147_getentrythemes.knowledgeentryid = KNOWLEDGEENTRYID #ArgumentGenerator 274
			api147_getentrythemesList = Api147GetentrythemesDao().api147_getentrythemes(api147_getentrythemes)
			api147_getentrythemeslistVar = api147_getentrythemesList if api147_getentrythemesList != None else []

			#選択済みテーマIDの配列を生成する
			themeIds = []
			for i in range(0, len(api147_getentrythemeslistVar)):
				rec = api147_getentrythemeslistVar[i]
				themeIds.append(utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "theme_id")))
			entryForm["theme_ids"] = themeIds

			#紐付ファイル選択用の原本文書一覧を取得する（API175_EntryFormInit）
			api175_entryforminitList = Api175EntryforminitDao().api175_entryforminit(Api175EntryforminitDto.dict_to_json({}))
			api175_entryforminitlistVar = api175_entryforminitList if api175_entryforminitList != None else []
			documentList = []
			for i in range(0, len(api175_entryforminitlistVar)):
				rec = api175_entryforminitlistVar[i]
				documentList.append({
					"knowledge_document_id": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "knowledge_document_id")),
					"document_code": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "document_code")),
					"title": utils.string_util.changeNullToBlank(utils.string_util.dict_get(rec, "title"))
				})

			#テーマ選択用のテーママスタ一覧を取得する（API120_GetThemes）
			themeList = Api120GetthemesDao().api120_getthemes(entryforminitapi_dto)
			if themeList is None :
				themeList = []

			#適用範囲選択用の県マスタ一覧を取得する（API100_GetPrefectureNames）
			prefectureList = Api100GetprefecturenamesDao().api100_getprefecturenames(entryforminitapi_dto)
			if prefectureList is None :
				prefectureList = []

			#日付型などJSON非対応オブジェクトはdefault=strで文字列化して返却する
			jsonObj.setHtml("entryForm", json.dumps(entryForm, default=str, ensure_ascii=False))
			jsonObj.setHtml("documentList", json.dumps(documentList, default=str, ensure_ascii=False))
			jsonObj.setHtml("themeList", json.dumps(themeList, default=str, ensure_ascii=False))
			jsonObj.setHtml("prefectureList", json.dumps(prefectureList, default=str, ensure_ascii=False))
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
