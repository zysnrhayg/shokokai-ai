#BasicService.vm
#make Service templete
# 報告書新規画面登録サービス
# trn_report および trn_report_theme へ報告書データを登録する
import json
import utils.config
import threading
import utils.json_constant
from flask import session
from sqlalchemy import text
from utils.mysqldb_utils import session_scope
from datetime import datetime, timezone, timedelta
import utils.date_util
from utils.jsonwfc_object import JSONWFCObject
import resources.messages
from app.dao.api124_insertreport.api124_insertreport_dao import Api124InsertreportDao
from app.dao.api125_insertreporttheme.api125_insertreporttheme_dao import Api125InsertreportthemeDao
from app.dto.api124_insertreport.api124_insertreport_dto import Api124InsertreportDto
from app.dto.api125_insertreporttheme.api125_insertreporttheme_dto import Api125InsertreportthemeDto
from app.dto.formnewsaveapi.formnewsaveapi_dto import FormnewsaveapiDto
from utils.save_data_check_utils import SaveDataCheckUtil
import utils.string_util


class FormnewsaveapiService :

	#
	# 報告書新規画面登録ボタン
	# @param Entity
	# @param jsonObj
	# @throws Exception
	#
	def formnewsaveapi(self,formnewsaveapi_dto,jsonObj) :

		#GeniusClientScript 1315
		FORM_CODE = formnewsaveapi_dto.formcode
		REPORT_DATE = formnewsaveapi_dto.reportdate
		TIME_START = formnewsaveapi_dto.timestart
		TIME_END = formnewsaveapi_dto.timeend
		STAFF_MAIN_CODE = formnewsaveapi_dto.staffmaincode
		STAFF_SUB_CODE = formnewsaveapi_dto.staffsubcode
		THEME_CODES = formnewsaveapi_dto.themecodes
		INDUSTRY = formnewsaveapi_dto.industry
		BUSINESS_NAME = formnewsaveapi_dto.businessname
		BUSINESS_PERSON = formnewsaveapi_dto.businessperson
		CONTENT = formnewsaveapi_dto.content
		SUMMARY = formnewsaveapi_dto.summary
		STATUS = formnewsaveapi_dto.status
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書新規画面登録ボタン_FormNewSaveAPI_(API)

			#「項目処理」（共通関数:FormNewSaveAPI）
			#パラメータは（form_code,report_date,time_start,time_end,staff_main_code,staff_sub_code,theme_codes,industry,business_name,business_person,content,summary,status）

			#以下の処理を行う。

			#セッションから年度ID・都道府県コード・商工会コードを取得する
			FISCAL_YEAR_ID = utils.string_util.changeNullToBlank(str(session.get("FISCAL_YEAR_ID") or ""))
			PREFECTURE_CODE = utils.string_util.changeNullToBlank(str(session.get("PREFECTURE_CODE") or ""))
			SHOKOKAI_CD = utils.string_util.changeNullToBlank(str(session.get("SHOKOKAI_CD") or ""))

			#報告書番号はINSERT後に採番されたreport_idから生成する（RPT-XXXX形式）
			#下書き保存と同一方式：先ず仮コードでINSERTし、report_id取得後にRPT-XXXXへ更新する
			REPORT_CODE = "RPT-TEMP"

			#担当者名を取得する（選択された担当者コードからmst_user_account.shokuin_kjを逆引きする）
			STAFF_MAIN_NAME = ""
			STAFF_SUB_NAME = ""
			with session_scope() as sess :
				if STAFF_MAIN_CODE :
					main_result = sess.execute(text("SELECT shokuin_kj FROM mst_user_account WHERE user_id = :user_id AND status = 1 AND deleted_at IS NULL LIMIT 1"), {'user_id': STAFF_MAIN_CODE})
					main_row = main_result.fetchone()
					if main_row :
						STAFF_MAIN_NAME = utils.string_util.changeNullToBlank(str(main_row[0] or ""))
				if STAFF_SUB_CODE :
					sub_result = sess.execute(text("SELECT shokuin_kj FROM mst_user_account WHERE user_id = :user_id AND status = 1 AND deleted_at IS NULL LIMIT 1"), {'user_id': STAFF_SUB_CODE})
					sub_row = sub_result.fetchone()
					if sub_row :
						STAFF_SUB_NAME = utils.string_util.changeNullToBlank(str(sub_row[0] or ""))

			#支援テーマIDを取得する（テーマコードからmst_theme.theme_idを逆引きする）
			THEME_ID = ""
			if THEME_CODES :
				theme_code_list = str(THEME_CODES).split(",")
				first_theme_code = theme_code_list[0].strip() if theme_code_list else ""
				if first_theme_code :
					with session_scope() as sess :
						theme_result = sess.execute(text("SELECT theme_id FROM mst_theme WHERE theme_code = :theme_code AND deleted_at IS NULL LIMIT 1"), {'theme_code': first_theme_code})
						theme_row = theme_result.fetchone()
						if theme_row :
							THEME_ID = str(theme_row[0])

			#必須項目のバリデーション
			if not FORM_CODE :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "帳票様式が選択されていません")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				return
			if not CONTENT :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "内容が未入力です")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				return
			#概要は内容と同一とする（概要フィールドは廃止）
			SUMMARY = CONTENT

			#trn_reportへ報告書データをINSERTし、採番されたreport_idから報告書番号を更新する
			#INSERTとUPDATEを同一トランザクション内で実行する（下書き保存と同一方式）
			REPORT_ID = ""
			with session_scope() as sess :
				#報告書データをINSERTする（仮コード'RPT-TEMP'で登録）
				#fiscal_year_idが未設定の場合は最新年度を自動取得する
				result = sess.execute(text("""INSERT INTO trn_report (
    report_code, form_code, fiscal_year_id, prefecture_code, shokokai_cd, theme_id, industry_code,
    report_date, summary, content, time_start, time_end, business_person, business_name,
    staff_main_name, staff_sub_name, registered_at, status, created_at, updated_at
) VALUES (
    'RPT-TEMP', NULLIF(:form_code, ''),
    COALESCE(NULLIF(:fiscal_year_id, '')::integer, (SELECT fiscal_year_id FROM mst_fiscal_year ORDER BY fiscal_year_code DESC, fiscal_year_id DESC LIMIT 1)),
    NULLIF(:prefecture_code, ''), NULLIF(:shokokai_cd, ''),
    NULLIF(:theme_id, '')::integer, NULLIF(:industry, ''),
    NULLIF(:report_date, '')::date, :summary, :content,
    NULLIF(:time_start, ''), NULLIF(:time_end, ''),
    NULLIF(:business_person, ''), NULLIF(:business_name, ''),
    NULLIF(:staff_main_name, ''), NULLIF(:staff_sub_name, ''),
    CURRENT_DATE, :status, to_char(now(), 'YYYYMMDDHH24MISS'), to_char(now(), 'YYYYMMDDHH24MISS')
) RETURNING report_id"""), {
					'form_code': FORM_CODE,
					'fiscal_year_id': FISCAL_YEAR_ID,
					'prefecture_code': PREFECTURE_CODE,
					'shokokai_cd': SHOKOKAI_CD,
					'theme_id': THEME_ID,
					'industry': INDUSTRY,
					'report_date': REPORT_DATE,
					'summary': SUMMARY,
					'content': CONTENT,
					'time_start': TIME_START,
					'time_end': TIME_END,
					'business_person': BUSINESS_PERSON,
					'business_name': BUSINESS_NAME,
					'staff_main_name': STAFF_MAIN_NAME,
					'staff_sub_name': STAFF_SUB_NAME,
					'status': STATUS,
				})
				row = result.fetchone()
				if row :
					REPORT_ID = str(row[0])

				#採番されたreport_idから報告書番号を「RPT-XXXX」形式で更新する
				if REPORT_ID :
					sess.execute(text("UPDATE trn_report SET report_code = 'RPT-' || LPAD(CAST(report_id AS text), 4, '0') WHERE report_id = CAST(:report_id AS integer)"), {'report_id': REPORT_ID})
					REPORT_CODE = "RPT-" + REPORT_ID.rjust(4, "0")

			#trn_report_themeへテーマ紐付けをINSERTする（theme_code→theme_id変換を行う）
			if REPORT_ID and THEME_CODES :
				theme_code_list = str(THEME_CODES).split(",")
				with session_scope() as sess :
					for tc in theme_code_list :
						tc = tc.strip()
						if not tc :
							continue
						#theme_codeからtheme_idを取得する
						t_result = sess.execute(text("SELECT theme_id FROM mst_theme WHERE theme_code = :tc AND deleted_at IS NULL LIMIT 1"), {'tc': tc})
						t_row = t_result.fetchone()
						if t_row :
							sess.execute(text("INSERT INTO trn_report_theme (report_id, theme_id) VALUES (CAST(:report_id AS integer), CAST(:theme_id AS integer)) ON CONFLICT DO NOTHING"), {'report_id': REPORT_ID, 'theme_id': str(t_row[0])})

			#登録結果をフロントエンドへ返却する
			jsonObj.setValue("dragReportId", REPORT_ID)
			jsonObj.setValue("dragReportCode", REPORT_CODE)
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "報告書を登録しました（報告書番号: " + REPORT_CODE + "）")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "報告書の登録に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
