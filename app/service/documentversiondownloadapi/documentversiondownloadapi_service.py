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
from app.dto.documentversiondownloadapi.documentversiondownloadapi_dto import DocumentversiondownloadapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util
from sqlalchemy import text
from utils.mysqldb_utils import Session


class DocumentversiondownloadapiService :

	#
	# ナレッジ文書詳細⬇ ダウンロード
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentversiondownloadapi(self,documentversiondownloadapi_dto,jsonObj) :

		# ダウンロード対象の文書IDと版番号を取得する
		ID = documentversiondownloadapi_dto.id
		VERSION = documentversiondownloadapi_dto.version
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#ナレッジ文書詳細⬇ ダウンロード_DocumentVersionDownloadAPI_(API)

			#「項目処理」（共通関数:DocumentVersionDownloadAPI）,パラメータは（id,version）

			#以下の処理を行う。

			# 文書版情報（ファイルパス、タイトル）をデータベースから取得する
			db_session = Session()
			try :
				result = db_session.execute(text("""SELECT d.title , v.file_path , v.file_size_kb , v.version_number FROM trn_knowledge_document d INNER JOIN trn_knowledge_document_version v ON v.knowledge_document_id = d.knowledge_document_id WHERE d.knowledge_document_id = :knowledge_document_id AND v.version_number = :version_number"""), {
					'knowledge_document_id': int(ID) if ID else 0,
					'version_number': int(VERSION) if VERSION else 1
				})
				row = result.fetchone()
			finally :
				Session.remove()

			# ダウンロード情報をフロントエンドに返却する
			if row :
				downloadInfo = {
					"title": str(row[0]) if row[0] else "",
					"file_path": str(row[1]) if row[1] else "",
					"file_size_kb": str(row[2]) if row[2] else "0",
					"version_number": str(row[3]) if row[3] else "1"
				}
			else :
				downloadInfo = {
					"title": "",
					"file_path": "",
					"file_size_kb": 0,
					"version_number": 1
				}
			jsonObj.setHtml("downloadInfo", json.dumps(downloadInfo, default=str, ensure_ascii=False))

			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
