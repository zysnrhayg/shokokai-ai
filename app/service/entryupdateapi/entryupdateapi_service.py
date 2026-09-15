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
from app.mapper.api145_updateknowledgeentry.api145_updateknowledgeentry_mapper import api145_updateknowledgeentryMapper
from app.dto.entryupdateapi.entryupdateapi_dto import EntryupdateapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util
from sqlalchemy import text
from utils.mysqldb_utils import Session




class EntryupdateapiService :

	#
	# 知識データ編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entryupdateapi(self,entryupdateapi_dto,jsonObj) :

		#GeniusClientScript 1315
		# フロントエンドから入力値を取得する（row配下）
		KNOWLEDGE_ENTRY_ID = entryupdateapi_dto.knowledgeentryid#GeninusClientScript 1318
		TITLE = entryupdateapi_dto.title#GeninusClientScript 1318
		KNOWLEDGE_DOCUMENT_ID = entryupdateapi_dto.knowledgedocumentid#GeninusClientScript 1318
		PREFECTURE_CODE = entryupdateapi_dto.prefecturecode#GeninusClientScript 1318
		CONTENT = entryupdateapi_dto.content#GeninusClientScript 1318
		THEME_IDS = entryupdateapi_dto.themeids#GeninusClientScript 1318
		STATUS = entryupdateapi_dto.status#GeninusClientScript 1318
		# updated_byはinteger型（user_account_id）
		USER_ACCOUNT_ID = session.get("USER_ACCOUNT_ID", 1) or 1
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ編集画面登録ボタン_EntryUpdateAPI_(API)

			#「項目処理」（共通関数:EntryUpdateAPI）,パラメータは（knowledge_entry_id,title,knowledge_document_id,content,theme_ids,status）

			#知識データIDが空の場合は更新しない
			if KNOWLEDGE_ENTRY_ID == "" or KNOWLEDGE_ENTRY_ID is None :
				raise ValueError("EntryUpdateAPI: knowledgeentryidが未指定のため更新できません")

			# prefecture_code・knowledge_document_idが空文字の場合はNULLにする（FK制約対応）
			pref_code = PREFECTURE_CODE if PREFECTURE_CODE and str(PREFECTURE_CODE).strip() else None
			doc_id = KNOWLEDGE_DOCUMENT_ID if KNOWLEDGE_DOCUMENT_ID not in ("", None) else None

			# テーマIDをカンマ区切り文字列から整数リストに変換する
			themeIdList = []
			if THEME_IDS :
				for tid in str(THEME_IDS).split(",") :
					tid = tid.strip()
					if tid != "" :
						themeIdList.append(int(tid))

			# 知識データ本体の更新とテーマ関連の再登録を同一トランザクションで行う
			db_session = Session()
			try :
				# trn_knowledge_entryテーブルを更新する（API145_UpdateKnowledgeEntry）
				update_sql = api145_updateknowledgeentryMapper.api145_updateknowledgeentry(
					TITLE, pref_code, doc_id, STATUS, CONTENT, USER_ACCOUNT_ID, KNOWLEDGE_ENTRY_ID)
				result = db_session.execute(text(update_sql), {
					'title': TITLE,
					'prefecturecode': pref_code,
					'knowledgedocumentid': doc_id,
					'status': STATUS,
					'content': CONTENT,
					'updatedby': USER_ACCOUNT_ID,
					'knowledgeentryid': KNOWLEDGE_ENTRY_ID
				})
				KOUSHINKENSUU = result.rowcount

				# テーマ関連を一度削除してから再登録する（全件入れ替え）
				db_session.execute(text("DELETE FROM trn_knowledge_entry_theme WHERE knowledge_entry_id = :knowledgeentryid"), {
					'knowledgeentryid': KNOWLEDGE_ENTRY_ID
				})
				for tid in themeIdList :
					db_session.execute(text("INSERT INTO trn_knowledge_entry_theme ( knowledge_entry_id , theme_id ) VALUES ( :knowledgeentryid , :themeid )"), {
						'knowledgeentryid': KNOWLEDGE_ENTRY_ID,
						'themeid': tid
					})

				db_session.commit()
			except Exception as e:
				db_session.rollback()
				raise e
			finally :
				Session.remove()

			#<更新件数>が"1"の場合,「更新しました」メッセージを表示する。
			#GeniusClientScript 983
			if str(KOUSHINKENSUU) == "1" : #GeniusContion 823
				#「更新しました」メッセージをフロントエンドに返却する。
				jsonObj.setHtml("msg", "知識データを更新しました")
				#処理終了。
			else :
				#更新対象が存在しない場合はエラーメッセージを返却する
				jsonObj.setHtml("msg", "更新対象の知識データが見つかりません")
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
