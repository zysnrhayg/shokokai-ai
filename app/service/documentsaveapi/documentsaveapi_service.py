#BasicService.vm
#make Service templete
import json
import os
import utils.config
import threading
import utils.json_constant
from flask import session
from app.common.getautonum import GetAutonum
from datetime import datetime, timezone, timedelta
import utils.date_util
from utils.jsonwfc_object import JSONWFCObject
import resources.messages
from app.dto.documentsaveapi.documentsaveapi_dto import DocumentsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util
import utils.file_util
from sqlalchemy import text
from utils.mysqldb_utils import Session


class DocumentsaveapiService :

	#
	# ナレッジ文書新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentsaveapi(self,documentsaveapi_dto,jsonObj) :

		# フロントエンドから入力値を取得する
		TITLE = documentsaveapi_dto.title
		CATEGORY = documentsaveapi_dto.category
		FORMAT = documentsaveapi_dto.format
		PREFECTURE_CODE = documentsaveapi_dto.prefecturecode
		FILE_PATH = documentsaveapi_dto.filepath
		FILE_SIZE_KB = documentsaveapi_dto.filesizekb
		STATUS = documentsaveapi_dto.status
		# ログインユーザーIDをFlaskセッションから取得する
		UPLOADED_BY = session.get('user_id', 'system') if hasattr(session, 'get') else 'system'

		# アップロードされた文書ファイルをUPLOAD_DIR（uploads/knowledge/）配下へ実保存する
		# 保存成功時は実ファイルパス・実サイズをDB登録値へ採用する
		DOCFILE = getattr(documentsaveapi_dto, "docfile", None)
		saved_rel_path = utils.file_util.save_upload_file(DOCFILE, "knowledge")
		if saved_rel_path :
			FILE_PATH = saved_rel_path
			abs_path = utils.file_util.get_upload_abs_path(saved_rel_path)
			FILE_SIZE_KB = str(max(1, int(os.path.getsize(abs_path) / 1024)))

		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書新規画面登録ボタン_DocumentSaveAPI_(API)

			#「項目処理」（共通関数:DocumentSaveAPI）,パラメータは（title,category,format,file）

			#以下の処理を行う。

			# 新規ナレッジ文書IDを自動採番する（MAX+1）
			db_session = Session()
			try :
				# 文書IDの自動採番（COALESCE(MAX(knowledge_document_id), 0) + 1）
				result = db_session.execute(text("SELECT COALESCE(MAX(knowledge_document_id), 0) + 1 AS new_id FROM trn_knowledge_document"))
				row = result.fetchone()
				KNOWLEDGE_DOCUMENT_ID = row[0] if row else 1

				# 文書コードの自動採番（doc-XXX形式）
				DOCUMENT_CODE = "doc-" + str(KNOWLEDGE_DOCUMENT_ID).zfill(3)

				# prefecture_codeが空文字の場合はNULLにする（FK制約対応）
				pref_code = PREFECTURE_CODE if PREFECTURE_CODE and PREFECTURE_CODE.strip() else None

				# trn_knowledge_documentテーブルに新規文書を登録する
				db_session.execute(text("""INSERT INTO trn_knowledge_document ( knowledge_document_id , prefecture_code , active_version_number , document_code , title , category , format , created_at , updated_at ) VALUES ( :knowledge_document_id , :prefecture_code , 1 , :document_code , :title , :category , :format , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) )"""), {
					'knowledge_document_id': KNOWLEDGE_DOCUMENT_ID,
					'prefecture_code': pref_code,
					'document_code': DOCUMENT_CODE,
					'title': TITLE,
					'category': CATEGORY,
					'format': FORMAT
				})

				# trn_knowledge_document_versionテーブルに初版を登録する
				db_session.execute(text("""INSERT INTO trn_knowledge_document_version ( knowledge_document_id , version_number , uploaded_date , uploaded_by , file_size_kb , status , file_path , created_at , updated_at ) VALUES ( :knowledge_document_id , 1 , CURRENT_DATE , :uploaded_by , :file_size_kb , :status , :file_path , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) , TO_CHAR ( NOW ( ) , 'YYYYMMDDHH24MISS' ) )"""), {
					'knowledge_document_id': KNOWLEDGE_DOCUMENT_ID,
					'uploaded_by': UPLOADED_BY,
					'file_size_kb': int(FILE_SIZE_KB) if FILE_SIZE_KB else 0,
					'status': STATUS if STATUS else '審査中',
					'file_path': FILE_PATH if FILE_PATH else ''
				})

				db_session.commit()
			except Exception as e:
				db_session.rollback()
				raise e
			finally :
				Session.remove()

			# 登録完了メッセージをフロントエンドに返却する
			jsonObj.setHtml("msg", "文書を登録しました")

			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
