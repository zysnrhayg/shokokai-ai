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
from app.mapper.api144_insertknowledgeentry.api144_insertknowledgeentry_mapper import api144_insertknowledgeentryMapper
from app.dto.entrysaveapi.entrysaveapi_dto import EntrysaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util
from sqlalchemy import text
from utils.mysqldb_utils import Session




class EntrysaveapiService :

	#
	# 知識データ新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def entrysaveapi(self,entrysaveapi_dto,jsonObj) :

		#GeniusClientScript 1315
		# フロントエンドから入力値を取得する（row配下）
		TITLE = entrysaveapi_dto.title#GeninusClientScript 1318
		KNOWLEDGE_DOCUMENT_ID = entrysaveapi_dto.knowledgedocumentid#GeninusClientScript 1318
		PREFECTURE_CODE = entrysaveapi_dto.prefecturecode#GeninusClientScript 1318
		CONTENT = entrysaveapi_dto.content#GeninusClientScript 1318
		THEME_IDS = entrysaveapi_dto.themeids#GeninusClientScript 1318
		STATUS = entrysaveapi_dto.status#GeninusClientScript 1318
		# created_by・updated_byはinteger型（user_account_id）
		USER_ACCOUNT_ID = session.get("USER_ACCOUNT_ID", 1) or 1
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#知識データ新規画面登録ボタン_EntrySaveAPI_(API)

			#「項目処理」（共通関数:EntrySaveAPI）,パラメータは（title,knowledge_document_id,content,theme_ids,status）

			#タイトルは必須とする
			if TITLE == "" or TITLE is None :
				raise ValueError("EntrySaveAPI: タイトルが未指定のため登録できません")

			# ステータスが未指定の場合は「下書き」を設定する
			if STATUS == "" or STATUS is None :
				STATUS = "下書き"

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

			# 知識データ本体の登録とテーマ関連の登録を同一トランザクションで行う
			db_session = Session()
			try :
				# trn_knowledge_entryテーブルに新規知識データを登録する（API144_InsertKnowledgeEntry）
				# ナレッジコード（KN-XXX）はRETURNINGされた知識データIDから自動生成する
				insert_sql = api144_insertknowledgeentryMapper.api144_insertknowledgeentry(
					TITLE, pref_code, doc_id, STATUS, CONTENT, USER_ACCOUNT_ID, USER_ACCOUNT_ID)
				result = db_session.execute(text(insert_sql), {
					'title': TITLE,
					'prefecturecode': pref_code,
					'knowledgedocumentid': doc_id,
					'status': STATUS,
					'content': CONTENT,
					'createdby': USER_ACCOUNT_ID,
					'updatedby': USER_ACCOUNT_ID
				})
				ins_row = result.fetchone()
				KNOWLEDGE_ENTRY_ID = ins_row[0] if ins_row else None

				# テーマが選択されている場合は中間表に登録する
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

			#「登録しました」メッセージをフロントエンドに返却する。
			jsonObj.setHtml("msg", "知識データを登録しました")
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
