#BasicService.vm
#make Service templete
# 傾聴内容変換AI文字起こしを内容欄に反映サービス
# 文字起こしテキストを内容欄へ反映可能な形式で返却する
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from utils.jsonwfc_object import JSONWFCObject
from app.dto.voiceinsertcontentapi.voiceinsertcontentapi_dto import VoiceinsertcontentapiDto
import utils.string_util


class VoiceinsertcontentapiService :

	#	#
	# 傾聴内容変換AI文字起こしを内容欄に反映
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def voiceinsertcontentapi(self,voiceinsertcontentapi_dto,jsonObj) :

		#GeniusClientScript 1315
		TRANSCRIPT = voiceinsertcontentapi_dto.transcript#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI文字起こしを内容欄に反映_VOICEINSERTCONTENTAPI_(API)

			#「項目処理」（共通関数:VOICEINSERTCONTENTAPI）,パラメータは（transcript）

			#以下の処理を行う。

			#文字起こしテキストの前後の空白を整えて返却する。
			transcript = utils.string_util.changeNullToBlank(TRANSCRIPT).strip()
			if not transcript :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "文字起こし結果がないため転記できません")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
				return

			#反映用テキスト（実データ）をフロントエンドへ返却する。
			jsonObj.setHtml("dragTranscript", transcript)
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "内容欄に反映しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "内容欄への反映に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
