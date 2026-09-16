#BasicService.vm
#make Service templete
# 傾聴内容変換AI音声録音 開始／停止サービス
# 録音の開始／停止をサーバー側で管理し、実タイムスタンプ（JST）を返却する
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from datetime import datetime, timezone, timedelta
from utils.jsonwfc_object import JSONWFCObject
from app.dto.voicerecordapi.voicerecordapi_dto import VoicerecordapiDto
import utils.string_util


class VoicerecordapiService :

	#	#
	# 報告書編集音声録音 開始／停止
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def voicerecordapi(self,voicerecordapi_dto,jsonObj) :

		#GeniusClientScript 1315
		ACTION = voicerecordapi_dto.action  # =START|STOP GeninusClientScript 1318
		REPORT_ID = voicerecordapi_dto.reportid  # 任意 GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集音声録音 開始／停止_VOICERECORDAPI_(API)

			#「項目処理」（共通関数:VOICERECORDAPI）,パラメータは（action=start|stop,report_id任意）

			#以下の処理を行う。

			action = utils.string_util.changeNullToBlank(ACTION).lower()
			if action not in ("start", "stop") :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "actionにはstartまたはstopを指定してください")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
				return

			#サーバー側現在時刻（日本時間）を取得する。
			jst_now = datetime.now(timezone(timedelta(hours=9)))
			recorded_at = jst_now.strftime("%Y-%m-%d %H:%M:%S")

			#録音状態と実タイムスタンプをセッションに保持し、フロントエンドへ返却する。
			if action == "start" :
				session["VOICE_RECORD_STARTED_AT"] = recorded_at
				session["VOICE_RECORD_REPORT_ID"] = utils.string_util.changeNullToBlank(REPORT_ID)
				jsonObj.setHtml("dragAction", "start")
				jsonObj.setHtml("dragStartedAt", recorded_at)
				jsonObj.setValue(utils.json_constant.JSONID_MSG, "録音を開始しました（" + recorded_at + "）")
			else :
				started_at = session.get("VOICE_RECORD_STARTED_AT", "")
				session["VOICE_RECORD_STARTED_AT"] = ""
				jsonObj.setHtml("dragAction", "stop")
				jsonObj.setHtml("dragStartedAt", utils.string_util.changeNullToBlank(started_at))
				jsonObj.setHtml("dragStoppedAt", recorded_at)
				jsonObj.setValue(utils.json_constant.JSONID_MSG, "録音を停止しました（" + recorded_at + "）")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "録音状態の更新に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
