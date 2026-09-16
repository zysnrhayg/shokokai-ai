#BasicService.vm
#make Service templete
# 傾聴内容変換AI音声ファイル アップロードサービス
# アップロードされた音声ファイルをサーバー（uploads/voice/）へ実保存し、保存結果を返却する
# 保存ファイルは30日後に削除される想定のため、削除予定日を併せて返す
import json
import os
import re
import uuid
import utils.config
import threading
import utils.json_constant
from flask import session
from datetime import datetime, timezone, timedelta
from utils.jsonwfc_object import JSONWFCObject
from app.dto.voiceuploadapi.voiceuploadapi_dto import VoiceuploadapiDto
import utils.string_util


class VoiceuploadapiService :

	# 音声ファイルの保存先（プロジェクトルート配下）
	UPLOAD_DIR_NAME = os.path.join("uploads", "voice")
	# 音声ファイルの保持期間（日数）
	RETENTION_DAYS = 30
	# 許可する拡張子
	ALLOWED_EXTENSIONS = (".wav", ".mp3", ".m4a", ".webm", ".ogg", ".aac")

	#	#
	# 報告書編集音声ファイル アップロード
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def voiceuploadapi(self,voiceuploadapi_dto,jsonObj) :

		#GeniusClientScript 1315
		AUDIO_FILE = voiceuploadapi_dto.audiofile  # (MULTIPART) GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集音声ファイル アップロード_VOICEUPLOADAPI_(API)

			#「項目処理」（共通関数:VOICEUPLOADAPI）,パラメータは（audio_file(multipart),report_id任意）

			#以下の処理を行う。

			if AUDIO_FILE is None :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "音声ファイルが指定されていません")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
				return

			#元ファイル名の拡張子を確認する（音声ファイルのみ許可）。
			original_name = utils.string_util.changeNullToBlank(getattr(AUDIO_FILE, "filename", "") or "audio.webm")
			ext = os.path.splitext(original_name)[1].lower()
			if ext not in VoiceuploadapiService.ALLOWED_EXTENSIONS :
				ext = ".webm"

			#保存先ディレクトリ（uploads/voice/YYYYMM）を用意する。
			jst_now = datetime.now(timezone(timedelta(hours=9)))
			upload_root = os.path.abspath(os.path.join(os.getcwd(), VoiceuploadapiService.UPLOAD_DIR_NAME))
			save_dir = os.path.join(upload_root, jst_now.strftime("%Y%m"))
			os.makedirs(save_dir, exist_ok=True)

			#保存ファイル名（voice_年月日_時分秒_ユニークID.拡張子）を生成し、実保存する。
			safe_base = re.sub(r"[^\w\-]", "_", os.path.splitext(original_name)[0])[:50]
			save_name = "voice_" + jst_now.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8] + "_" + (safe_base or "audio") + ext
			save_path = os.path.join(save_dir, save_name)
			AUDIO_FILE.save(save_path)

			#保存ファイルの実サイズを取得する。
			file_size = os.path.getsize(save_path)

			#削除予定日（作成日から30日後）を算出する。
			delete_date = jst_now + timedelta(days=VoiceuploadapiService.RETENTION_DAYS)

			#保存結果（実データ）をフロントエンドへ返却する。
			jsonObj.setHtml("dragFileName", save_name)
			jsonObj.setHtml("dragFileSize", str(file_size))
			jsonObj.setHtml("dragDeleteDate", delete_date.strftime("%Y-%m-%d"))
			jsonObj.setHtml("dragRecordedAt", jst_now.strftime("%Y-%m-%d %H:%M"))
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "音声ファイルを保存しました（" + save_name + "）")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "音声ファイルのアップロードに失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
