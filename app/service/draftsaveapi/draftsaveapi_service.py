#BasicService.vm
#make Service templete
# 傾聴内容変換AI下書き保存サービス
# 報告書項目一式をDB（trn_report＋trn_report_theme）へ下書き（status='下書き'）として登録する
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from sqlalchemy import text
from utils.jsonwfc_object import JSONWFCObject
from utils.mysqldb_utils import session_scope
from app.dto.draftsaveapi.draftsaveapi_dto import DraftsaveapiDto
import utils.string_util
from datetime import datetime, timezone, timedelta
import utils.date_util


class DraftsaveapiService :

	#	#
	# 傾聴内容変換AI下書き保存
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def draftsaveapi(self,draftsaveapi_dto,jsonObj) :

		#GeniusClientScript 1315
		HOUKOKUSHOKOUMOKUISSHIKI = draftsaveapi_dto.houkokushokoumokuisshiki#GeninusClientScript 1318
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#傾聴内容変換AI下書き保存_DRAFTSAVEAPI_(API)

			#「項目処理」（共通関数:DRAFTSAVEAPI）,パラメータは（報告書項目一式）

			#以下の処理を行う。

			#報告書項目一式から登録値を取り出す（未指定は空文字とする）。
			fields = HOUKOKUSHOKOUMOKUISSHIKI if isinstance(HOUKOKUSHOKOUMOKUISSHIKI, dict) else {}
			form_code = utils.string_util.changeNullToBlank(fields.get("formcode", ""))
			report_date = utils.string_util.changeNullToBlank(fields.get("reportdate", ""))
			time_start = utils.string_util.changeNullToBlank(fields.get("timestart", ""))
			time_end = utils.string_util.changeNullToBlank(fields.get("timeend", ""))
			business_name = utils.string_util.changeNullToBlank(fields.get("businessname", ""))
			industry_code = utils.string_util.changeNullToBlank(fields.get("industrycode", ""))
			staff_main_name = utils.string_util.changeNullToBlank(fields.get("staffmainname", ""))
			staff_sub_name = utils.string_util.changeNullToBlank(fields.get("staffsubname", ""))
			content = utils.string_util.changeNullToBlank(fields.get("content", ""))
			summary = utils.string_util.changeNullToBlank(fields.get("summary", ""))
			voice_transcript = utils.string_util.changeNullToBlank(fields.get("voicetranscript", ""))
			theme_codes = fields.get("themecodes", []) if isinstance(fields.get("themecodes", []), list) else []
			# report_id指定時（既存下書きの更新）はUPDATE、未指定時はINSERTとする。
			report_id = utils.string_util.changeNullToBlank(str(fields.get("reportid", "") or ""))

			#セッションの組織情報・ユーザー情報を取得する。
			prefecture_code = utils.string_util.changeNullToBlank(session.get("PREFECTURE_CODE") or "")
			shokokai_cd = utils.string_util.changeNullToBlank(session.get("SHOKOKAI_CD") or "")
			user_account_id = utils.string_util.changeNullToBlank(str(session.get("USER_ACCOUNT_ID") or ""))

			#内容（content）が空の場合は登録しない（summaryはNOT NULLのため内容の先頭部分で補完する）。
			if not content :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "内容が未入力のため下書き保存できません")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
				return
			if not summary :
				summary = content[:100]

			#トランザクション内で下書き（trn_report）と支援テーマ（trn_report_theme）を登録する。
			#report_codeは採番後のreport_idから「RPT-XXXX」形式で生成する。
			with session_scope() as sess :
				if report_id :
					#既存下書きの更新（report_id指定時）
					update_sql = text("""UPDATE trn_report
SET form_code = :form_code
  , report_date = NULLIF(:report_date, '')::date
  , time_start = NULLIF(:time_start, '')
  , time_end = NULLIF(:time_end, '')
  , business_name = NULLIF(:business_name, '')
  , industry_code = NULLIF(:industry_code, '')
  , staff_main_name = NULLIF(:staff_main_name, '')
  , staff_sub_name = NULLIF(:staff_sub_name, '')
  , content = :content
  , summary = :summary
  , voice_transcript = NULLIF(:voice_transcript, '')
  , updated_at = NOW()
  , updated_by = :updated_by
WHERE report_id = CAST(:report_id AS integer)
  AND status = '下書き'
  AND deleted_at IS NULL""")
					sess.execute(update_sql, {
						'form_code': form_code,
						'report_date': report_date,
						'time_start': time_start,
						'time_end': time_end,
						'business_name': business_name,
						'industry_code': industry_code,
						'staff_main_name': staff_main_name,
						'staff_sub_name': staff_sub_name,
						'content': content,
						'summary': summary,
						'voice_transcript': voice_transcript,
						'updated_by': int(user_account_id) if user_account_id else None,
						'report_id': report_id,
					})
					#既存の支援テーマ紐付けを一度削除してから登録し直す。
					sess.execute(text("DELETE FROM trn_report_theme WHERE report_id = CAST(:report_id AS integer)"), {'report_id': report_id})
				else :
					#新規下書きの登録（INSERT ... RETURNING report_id）
					insert_sql = text("""INSERT INTO trn_report
(report_code, fiscal_year_id, prefecture_code, shokokai_cd, form_code, report_date, time_start, time_end,
 business_name, industry_code, staff_main_name, staff_sub_name, content, summary, voice_transcript,
 status, registered_at, created_at, created_by)
VALUES
('RPT-TEMP', (SELECT fiscal_year_id FROM mst_fiscal_year ORDER BY fiscal_year_code DESC, fiscal_year_id DESC LIMIT 1),
 :prefecture_code, :shokokai_cd, NULLIF(:form_code, ''), NULLIF(:report_date, '')::date, NULLIF(:time_start, ''), NULLIF(:time_end, ''),
 NULLIF(:business_name, ''), NULLIF(:industry_code, ''), NULLIF(:staff_main_name, ''), NULLIF(:staff_sub_name, ''),
 :content, :summary, NULLIF(:voice_transcript, ''),
 '下書き', NOW(), NOW(), :created_by)
RETURNING report_id""")
					result = sess.execute(insert_sql, {
						'prefecture_code': prefecture_code,
						'shokokai_cd': shokokai_cd,
						'form_code': form_code,
						'report_date': report_date,
						'time_start': time_start,
						'time_end': time_end,
						'business_name': business_name,
						'industry_code': industry_code,
						'staff_main_name': staff_main_name,
						'staff_sub_name': staff_sub_name,
						'content': content,
						'summary': summary,
						'voice_transcript': voice_transcript,
						'created_by': int(user_account_id) if user_account_id else None,
					})
					row = result.fetchone()
					report_id = str(row[0]) if row else ""
					#report_codeを採番したreport_idから「RPT-XXXX」形式で更新する。
					sess.execute(text("UPDATE trn_report SET report_code = 'RPT-' || LPAD(CAST(report_id AS text), 4, '0') WHERE report_id = CAST(:report_id AS integer)"), {'report_id': report_id})

				#支援テーマ（theme_code→mst_theme.theme_id）を紐付ける。
				for theme_code in theme_codes :
					theme_code = utils.string_util.changeNullToBlank(str(theme_code or ""))
					if not theme_code :
						continue
					sess.execute(text("""INSERT INTO trn_report_theme (report_id, theme_id)
SELECT CAST(:report_id AS integer), t.theme_id
FROM mst_theme t
WHERE t.theme_code = :theme_code AND t.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM trn_report_theme x WHERE x.report_id = CAST(:report_id AS integer) AND x.theme_id = t.theme_id)"""),
						{'report_id': report_id, 'theme_code': theme_code})

			#採番したreport_idをフロントエンドへ返却する。
			jsonObj.setHtml("dragReportId", report_id)
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "下書きを保存しました（報告書ID: " + report_id + "）")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "下書きの保存に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
