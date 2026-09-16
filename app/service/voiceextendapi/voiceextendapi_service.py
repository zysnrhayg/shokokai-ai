#BasicService.vm
#make Service templete
# 傾聴内容変換AI録音時間 ＋30分延長サービス
# サーバー側で延長後の録音時間（timer_remaining／timer_total）を算出して返却する
# 上限は60分（3600秒）とする
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from utils.jsonwfc_object import JSONWFCObject
from app.dto.voiceextendapi.voiceextendapi_dto import VoiceextendapiDto
import utils.string_util


class VoiceextendapiService :

	# 録音時間の上限（秒）
	MAX_TIMER_SECONDS = 3600

	#	#
	# 報告書編集録音時間 ＋30分延長
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def voiceextendapi(self,voiceextendapi_dto,jsonObj) :

		#GeniusClientScript 1315
		REPORT_ID = voiceextendapi_dto.reportid  # 任意 GeninusClientScript 1318
		ADD_SECONDS = voiceextendapi_dto.addseconds#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集録音時間 ＋30分延長_VOICEEXTENDAPI_(API)

			#「項目処理」（共通関数:VOICEEXTENDAPI）,パラメータは（report_id任意,add_seconds）

			#以下の処理を行う。

			#タイマーを延長しtimer_remaining/timer_totalを返す。

			#現在の残り時間・合計時間（未指定時は既定値30分）を取得する。
			try :
				timer_remaining = int(utils.string_util.changeNullToBlank(str(voiceextendapi_dto.timeremaining)) or 1800)
			except ValueError :
				timer_remaining = 1800
			try :
				timer_total = int(utils.string_util.changeNullToBlank(str(voiceextendapi_dto.timetotal)) or 1800)
			except ValueError :
				timer_total = 1800
			try :
				add_seconds = int(utils.string_util.changeNullToBlank(str(ADD_SECONDS)) or 1800)
			except ValueError :
				add_seconds = 1800

			#上限（3600秒）を超えない範囲で延長する。
			addable = max(0, VoiceextendapiService.MAX_TIMER_SECONDS - timer_total)
			actual_add = min(add_seconds, addable)
			timer_total += actual_add
			timer_remaining += actual_add

			#延長後の録音時間（実データ）をフロントエンドへ返却する。
			jsonObj.setHtml("dragTimerRemaining", str(timer_remaining))
			jsonObj.setHtml("dragTimerTotal", str(timer_total))
			jsonObj.setHtml("dragAddedSeconds", str(actual_add))
			if actual_add <= 0 :
				jsonObj.setValue(utils.json_constant.JSONID_MSG, "録音時間は上限（60分）に達しています")
			else :
				jsonObj.setValue(utils.json_constant.JSONID_MSG, "録音時間を" + str(actual_add // 60) + "分延長しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "録音時間の延長に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
