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
from app.dao.api139_updateknowledgedocument.api139_updateknowledgedocument_dao import Api139UpdateknowledgedocumentDao
from app.dao.api_knowledgedocumentversioninformation.api_knowledgedocumentversioninformation_dao import ApiKnowledgedocumentversioninformationDao
from app.dto.api139_updateknowledgedocument.api139_updateknowledgedocument_dto import Api139UpdateknowledgedocumentDto
from app.dto.api_knowledgedocumentversioninformation.api_knowledgedocumentversioninformation_dto import ApiKnowledgedocumentversioninformationDto
from app.dto.documentupdateapi.documentupdateapi_dto import DocumentupdateapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util


class DocumentupdateapiService :

	#
	# ナレッジ文書編集画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def documentupdateapi(self,documentupdateapi_dto,jsonObj) :

		# 編集画面の入力値（原本文書ID・タイトル・カテゴリ・形式・適用範囲・ステータス）
		KNOWLEDGE_DOCUMENT_ID = documentupdateapi_dto.knowledgedocumentid
		TITLE = documentupdateapi_dto.title
		CATEGORY = documentupdateapi_dto.category
		FORMAT = documentupdateapi_dto.format
		PREFECTURE_CODE = documentupdateapi_dto.prefecturecode or ""
		STATUS = documentupdateapi_dto.status or ""
		# updated_byはinteger型（user_account_id）
		USER_ACCOUNT_ID = session.get("USER_ACCOUNT_ID", 1) or 1
		api139_updateknowledgedocument = Api139UpdateknowledgedocumentDto.dict_to_json({})
		api_knowledgedocumentversioninformation = ApiKnowledgedocumentversioninformationDto.dict_to_json({})

		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			# ナレッジ文書編集画面登録ボタン_DocumentUpdateAPI_(API)

			# 原本文書マスタを更新する（タイトル・適用範囲・カテゴリ・形式・更新者）
			api139_updateknowledgedocument.title = TITLE
			api139_updateknowledgedocument.prefecturecode = PREFECTURE_CODE
			api139_updateknowledgedocument.category = CATEGORY
			api139_updateknowledgedocument.format = FORMAT
			api139_updateknowledgedocument.updatedby = USER_ACCOUNT_ID
			api139_updateknowledgedocument.knowledgedocumentid = KNOWLEDGE_DOCUMENT_ID
			Api139UpdateknowledgedocumentDao().api139_updateknowledgedocument(api139_updateknowledgedocument)

			# 有効版のステータスを更新する（ステータスが指定されている場合のみ）
			if STATUS != "" :
				api_knowledgedocumentversioninformation.status = STATUS
				api_knowledgedocumentversioninformation.updatedby = USER_ACCOUNT_ID
				api_knowledgedocumentversioninformation.knowledgedocumentid = KNOWLEDGE_DOCUMENT_ID
				ApiKnowledgedocumentversioninformationDao().api_knowledgedocumentversioninformation(api_knowledgedocumentversioninformation)

			# 「更新しました」メッセージを表示する
			jsonObj.setScript(utils.json_constant.JSONID_MSG, "更新しました")

		except Exception as e:
			utils.config.global_log.error(e)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
