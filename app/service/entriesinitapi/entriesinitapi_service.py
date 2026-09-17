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
from app.dao.api_chishikidetaichiran.api_chishikidetaichiran_dao import ApiChishikidetaichiranDao
from app.dto.api_chishikidetaichiran.api_chishikidetaichiran_dto import ApiChishikidetaichiranDto
from app.dto.entriesinitapi.entriesinitapi_dto import EntriesinitapiDto
from app.accounts.services import resolve_account_role
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util




class EntriesinitapiService :

	#
	# 知識データ一覧画面初期表示
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entriesinitapi(self,entriesinitapi_dto,jsonObj) :

		api_chishikidetaichiran = ApiChishikidetaichiranDto.dict_to_json({}) #CommonFunction 110
		# 県連ロールの場合、全国共有（prefecture_code IS NULL）＋自県分のみに絞込
		if resolve_account_role() == "pref" :
			api_chishikidetaichiran.prefecturecode = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE"))
		api_chishikidetaichiranList = None #ResultGenerator 72
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ一覧画面初期表示_EntriesInitAPI_(API)

			#関数「API_ChishikiDetaIchiran」の「db_API_ChishikiDetaIchiran」メソッドを行う,知識データ一覧を取得する。
			api_chishikidetaichiranList = ApiChishikidetaichiranDao().api_chishikidetaichiran(api_chishikidetaichiran)
			api_chishikidetaichiranlistVar = None #ResultGenerator 89
			if api_chishikidetaichiranList != None :
				api_chishikidetaichiranlistVar = api_chishikidetaichiranList.fetchall() if hasattr(api_chishikidetaichiranList, 'fetchall') else api_chishikidetaichiranList

			#取得結果をGrid「entries」用のJSON形式に変換する（20行ごとの改ページはフロントエンド側で行う）
			mapList = [] #GeniusGrid 606
			if api_chishikidetaichiranlistVar != None and len(api_chishikidetaichiranlistVar) > 0 :#GeniusGrid 647
				for i in range(0, len(api_chishikidetaichiranlistVar)): #GeniusGrid 652
					entity = api_chishikidetaichiranlistVar[i]
					selMap ={} #GeniusGrid681
					# 知識データID
					selMap["knowledge_entry_id"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "knowledge_entry_id"))
					# ナレッジコード
					selMap["knowledge_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "knowledge_code"))
					# タイトル
					selMap["title"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "title"))
					# 適用範囲（県コード・県名）
					selMap["prefecture_code"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "prefecture_code"))
					selMap["prefecture_name"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "prefecture_name"))
					# 紐付ファイル（原本文書）
					selMap["knowledge_document_id"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "knowledge_document_id"))
					selMap["document_title"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "document_title"))
					# テーマバッジ（中間表経由のJSON配列）
					theme_badges = utils.string_util.dict_get(entity, "theme_badges")
					if isinstance(theme_badges, str) :
						# json_aggの結果は文字列として返るためそのまま設定する
						selMap["theme_badges"] = theme_badges
					else :
						selMap["theme_badges"] = json.dumps(theme_badges if theme_badges else [], ensure_ascii=False)
					# 更新日
					selMap["updated_date"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "updated_date"))
					# ステータス
					selMap["status"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "status"))
					# 本文
					selMap["content"] = utils.string_util.changeNullToBlank(utils.string_util.dict_get(entity, "content"))
					mapList.insert(len(mapList),selMap)
			# 日付型などJSON非対応オブジェクトはdefault=strで文字列化する
			result = json.dumps(mapList, default=str, ensure_ascii=False)
			# 取得結果をフロントエンドのGrid「dragB」に返却する
			jsonObj.setHtml("dragB", result) #GeniusGrid748
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
