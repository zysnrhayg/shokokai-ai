# 専門家報告取込サービス
# アップロードされたファイル名と様式コードから、帳票・支援テーマ・日時・概要を生成しセッションへ保存する
import utils.config
import threading
import utils.json_constant
from flask import session
from datetime import datetime
from utils.jsonwfc_object import JSONWFCObject


class ExpertimportapiService:

	def expertimportapi(self, expertimportapi_dto, jsonObj):

		FILENAME = expertimportapi_dto.filename
		FORM_CODE = expertimportapi_dto.formcode
		utils.config.global_log.debug(str(threading.current_thread().native_id) + ": start")
		try:
			# 様式コードのバリデーション
			if FORM_CODE not in ('G-4', 'G-5'):
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "様式コードが不正です")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				return

			if not FILENAME:
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "ファイル名が指定されていません")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				return

			# 様式に応じて支援テーマコードを決定する
			THEME_CODE = 'labor' if FORM_CODE == 'G-4' else 'invoice'

			# 対応日・時刻・概要を生成する
			REPORT_DATE = datetime.now().strftime('%Y-%m-%d')
			TIME_START = '10:00'
			TIME_END = '11:00'
			SUMMARY = FILENAME + ' を取り込みました。内容をご確認のうえ入力してください'

			# セッションへ保存する
			session['EXPERT_IMPORT'] = {
				'formcode': FORM_CODE,
				'themecode': THEME_CODE,
				'reportdate': REPORT_DATE,
				'timestart': TIME_START,
				'timeend': TIME_END,
				'summary': SUMMARY,
			}

			# フロントエンドへ返却する
			jsonObj.setValue("dragFormCode", FORM_CODE)
			jsonObj.setValue("dragThemeCode", THEME_CODE)
			jsonObj.setValue("dragReportDate", REPORT_DATE)
			jsonObj.setValue("dragTimeStart", TIME_START)
			jsonObj.setValue("dragTimeEnd", TIME_END)
			jsonObj.setValue("dragSummary", SUMMARY)
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "専門家報告の取り込みに失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id) + ": end")
