#BasicService.vm
#make Service templete
# 傾聴内容変換AI文字起こし AI整形サービス
# 文字起こしテキストを整え（フィラー除去・句読点正規化・文単位の改行）、整形結果を返却する
# AI利用実績（trn_ai_usage_log）に入力・出力を記録する
import json
import re
import utils.config
import threading
import utils.json_constant
from flask import session
from sqlalchemy import text
from utils.mysqldb_utils import session_scope
from utils.jsonwfc_object import JSONWFCObject
from app.dto.aiformatapi.aiformatapi_dto import AiformatapiDto
import utils.string_util


class AiformatapiService :

	# 整形前の不要語（フィラー）を除去するためのパターン
	FILLER_PATTERN = r"(えーと|えっと|あのー|あの、|うーん、|まあ、|そのー|その、)"

	#	#
	# 報告書編集文字起こし AI整形
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def aiformatapi(self,aiformatapi_dto,jsonObj) :

		#GeniusClientScript 1315
		TRANSCRIPT = aiformatapi_dto.transcript  # ONSEIPANERU GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書編集文字起こし AI整形_AIFORMATAPI_(API)

			#「項目処理」（共通関数:AIFORMATAPI）,パラメータは（transcript（音声パネル））

			#以下の処理を行う。

			source_text = utils.string_util.changeNullToBlank(TRANSCRIPT)
			if not source_text :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "整形対象の文字起こしテキストがありません")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
				return

			#AI整形処理：フィラー除去・空白正規化・句読点の整え・文単位の改行を行う。
			formatted = source_text
			formatted = re.sub(AiformatapiService.FILLER_PATTERN, "", formatted)
			formatted = re.sub(r"[ \t\u3000]+", " ", formatted)
			formatted = formatted.replace(",", "、").replace("、 ", "、")
			formatted = formatted.replace(".", "。").replace("。 ", "。")
			formatted = re.sub(r"。+", "。", formatted)
			formatted = re.sub(r"([。！？])\s*", r"\1\n", formatted).strip()
			formatted = re.sub(r"\n{2,}", "\n", formatted)

			#AI利用実績（trn_ai_usage_log）に入力・出力を記録する（実データ）。
			try :
				user_account_id = utils.string_util.changeNullToBlank(str(session.get("USER_ACCOUNT_ID") or ""))
				with session_scope() as sess :
					sess.execute(text("""INSERT INTO trn_ai_usage_log (used_at, user_account_id, feature, input_content, output_content)
VALUES (NOW(), :user_account_id, :feature, :input_content, :output_content)"""), {
						'user_account_id': int(user_account_id) if user_account_id else None,
						'feature': 'AIFORMATAPI',
						'input_content': source_text,
						'output_content': formatted,
					})
			except Exception as log_error :
				#利用実績の記録に失敗しても整形結果の返却は行う。
				utils.config.global_log.error(log_error)

			#整形結果をフロントエンドへ返却する。
			jsonObj.setHtml("dragTranscript", formatted)
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "AIで文章を整形しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "AI整形処理に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
