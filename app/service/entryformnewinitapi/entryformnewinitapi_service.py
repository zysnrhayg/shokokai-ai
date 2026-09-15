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
from app.dao.api175_entryforminit.api175_entryforminit_dao import Api175EntryforminitDao
from app.dao.api120_getthemes.api120_getthemes_dao import Api120GetthemesDao
from app.dao.api100_getprefecturenames.api100_getprefecturenames_dao import Api100GetprefecturenamesDao
from app.dto.api175_entryforminit.api175_entryforminit_dto import Api175EntryforminitDto
from app.dto.entryformnewinitapi.entryformnewinitapi_dto import EntryformnewinitapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntryformnewinitapiService :

	#
	# 知識データ新規＋ 知識データを登録
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entryformnewinitapi(self,entryformnewinitapi_dto,jsonObj) :

		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ新規＋ 知識データを登録_EntryFormNewInitAPI_(API)

			#「項目処理」（共通関数:EntryFormNewInitAPI）,パラメータは（）

			#新規登録画面は知識データIDを持たないため、選択用マスタ一覧のみを返却する。

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
			themeList = Api120GetthemesDao().api120_getthemes(entryformnewinitapi_dto)
			if themeList is None :
				themeList = []

			#適用範囲選択用の県マスタ一覧を取得する（API100_GetPrefectureNames）
			prefectureList = Api100GetprefecturenamesDao().api100_getprefecturenames(entryformnewinitapi_dto)
			if prefectureList is None :
				prefectureList = []

			#日付型などJSON非対応オブジェクトはdefault=strで文字列化して返却する
			jsonObj.setHtml("documentList", json.dumps(documentList, default=str, ensure_ascii=False))
			jsonObj.setHtml("themeList", json.dumps(themeList, default=str, ensure_ascii=False))
			jsonObj.setHtml("prefectureList", json.dumps(prefectureList, default=str, ensure_ascii=False))
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
