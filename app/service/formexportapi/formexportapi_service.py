#BasicService.vm
#make Service templete
# 傾聴内容変換AI帳票出力サービス
# 指定された報告書（report_id）または最新の報告書をDB（v_output_reports_csv）から取得し、Excel出力する
import json
import os
import io
import tempfile
import utils.config
import threading
import utils.json_constant
from flask import session
from utils.jsonwfc_object import JSONWFCObject
from app.dao.api204_formexport.api204_formexport_dao import Api204FormexportDao
from app.dto.api204_formexport.api204_formexport_dto import Api204FormexportDto
from app.dto.formexportapi.formexportapi_dto import FormexportapiDto
import utils.string_util
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill


class FormexportapiService :

	#	#
	# 傾聴内容変換AI帳票出力
	# @param Entity
	# @param jsonObj
	# @return Excelファイルパス（失敗時はNone）
	# @throws Exception
	#
	def formexportapi(self,formexportapi_dto,jsonObj) :

		#GeniusClientScript 1315
		REPORT_ID = formexportapi_dto.reportid  # 任意 GeninusClientScript 1318
		FORM_CODE = formexportapi_dto.formcode  # 帳票コード（任意）
		SOURCE = formexportapi_dto.source  # 画面ソース（任意：ai-input or manual-input）
		#UltimateGeniuBean 115
		utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": start")
		try :
			#報告書新規帳票出力_FORMEXPORTAPI_(API)

			#「項目処理」（共通関数:FORMEXPORTAPI）,パラメータは（report_id任意,form_code任意,source任意）

			#以下の処理を行う。

			#関数「API204_FORMEXPORT」：帳票出力対象の報告書データを取得する。
			#画面ソースに応じてビューを切替する：
			#   ai-input（相談を受ける）→ v_output_f_excel（F相談受付票専用）
			#   manual-input（報告書を作る）→ v_output_reports_csv（formcode指定時は該当様式限定）
			api204_formexport = Api204FormexportDto.dict_to_json({})
			api204_formexport.reportid = utils.string_util.changeNullToBlank(REPORT_ID)
			api204_formexport.source = utils.string_util.changeNullToBlank(SOURCE)
			api204_formexport.formcode = utils.string_util.changeNullToBlank(FORM_CODE)
			api204_formexportList = Api204FormexportDao().api204_formexport(api204_formexport)

			#取得結果（1件）を確認する。
			report_row = {}
			if api204_formexportList :
				report_row = api204_formexportList[0]

			if not report_row :
				jsonObj.setValue(utils.json_constant.JSONID_ERR, "出力対象の報告書が見つかりません。先に下書き保存または登録を行ってください")
				jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
				utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")
				return None

			#帳票コードを取得する（DTO指定時優先、未指定時は取得データの「様式」から推定）。
			form_code = utils.string_util.changeNullToBlank(FORM_CODE)
			if not form_code :
				#取得データから帳票コードを推定する（「様式」フィールドの先頭文字を利用）。
				form_code = utils.string_util.changeNullToBlank(str(report_row.get("様式", "") or ""))

			#帳票コードに応じたASCIIファイル名前置を取得する。
			file_prefix = self._get_file_prefix(form_code)
			#帳票コードに応じたExcelタイトル（日文）を取得する。
			excel_title = self._get_excel_title(form_code)

			#Excel生成：取得データから帳票Excelファイルを出力する。
			file_path = self._generate_excel(report_row, excel_title)

			#出力ファイル名を設定する（日文は文字化け防止のためASCII名とする）。
			report_code = utils.string_util.changeNullToBlank(report_row.get("報告書番号", ""))
			file_name = file_prefix + "_" + report_code + ".xlsx"
			jsonObj.setValue("dragFileName", file_name)
			jsonObj.setValue(utils.json_constant.JSONID_MSG, "帳票出力が完了しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_SUCCESS)
			#処理終了。
			return file_path

		except Exception as e:
			utils.config.global_log.error(e)
			jsonObj.setValue(utils.json_constant.JSONID_ERR, "帳票出力に失敗しました")
			jsonObj.setValue(utils.json_constant.JSONID_FOR_RUNRESULT, utils.json_constant.RUNRESULT_FAIL)
			raise
		#utils.config.global_log.debug(str(threading.current_thread().native_id)+ ": end")

	# 帳票コードに応じたファイル名前置（帳票コード＋帳票名）を返す。
	# ファイル名形式：{帳票コード}_{帳票名}_{報告書番号}.xlsx
	# 例：F_相談受付票_RPT-0120.xlsx
	def _get_file_prefix(self, form_code) :
		# 帳票コード → 帳票名マッピング
		prefix_map = {
			"F": "F_相談受付票",
			"G-2": "G-2_事業所個別相談報告票",
			"G-3": "G-3_商工会だより作成報告票",
			"G-4": "G-4_専門家活用事業報告票",
			"G-5": "G-5_専門家派遣事業報告票",
			"G-6": "G-6_施策普及事業報告票",
			"G-7": "G-7_施策普及員報告票",
			"G-8": "G-8_事業実施に係る事務処理報告票",
			"H": "H_経営力強化支援事業報告票",
			"I-1": "I-1_商工会計画・実績表",
			"I-2": "I-2_小規模事業者経営改善資金助成",
			"I-3": "I-3_小規模企業者等設備投資補助",
			"I-4": "I-4_経営改良事業補助",
			"I-5": "I-5_事業再構築補助",
			"I-6": "I-6_地域中小企業振興資金助成",
			"I-7": "I-7_中小企業支援センター等設置事業",
			"I-8": "I-8_中小企業支援拠点整備事業",
		}
		# マッピングに存在する場合は前置を返す、未存在の場合は帳票コードをそのまま返す。
		if form_code in prefix_map :
			return prefix_map[form_code]
		return form_code or "報告書"

	# 帳票コードに応じたExcelタイトル（日文）を返す。
	def _get_excel_title(self, form_code) :
		# 帳票コード → Excel表示タイトルマッピング
		title_map = {
			"F": "F 相談受付票",
			"G-2": "G-2 事業所個別相談報告票",
			"G-3": "G-3 商工会だより作成報告票",
			"G-4": "G-4 専門家活用事業報告票",
			"G-5": "G-5 専門家派遣事業報告票",
			"G-6": "G-6 施策普及事業報告票",
			"G-7": "G-7 施策普及員報告票",
			"G-8": "G-8 事業実施に係る事務処理報告票",
			"H": "H 経営力強化支援事業報告票",
			"I-1": "I-1 商工会計画・実績表",
			"I-2": "I-2 小規模事業者経営改善資金助成",
			"I-3": "I-3 小規模企業者等設備投資補助",
			"I-4": "I-4 経営改良事業補助",
			"I-5": "I-5 事業再構築補助",
			"I-6": "I-6 地域中小企業振興資金助成",
			"I-7": "I-7 中小企業支援センター等設置事業",
			"I-8": "I-8 中小企業支援拠点整備事業",
		}
		# マッピングに存在する場合はタイトルを返す、未存在の場合は帳票コードを返す。
		if form_code in title_map :
			return title_map[form_code]
		return form_code or "報告書"

	# v_output_reports_csvの取得データからExcelファイルを生成する。
	def _generate_excel(self, row, excel_title="報告書") :
		wb = Workbook()
		ws = wb.active
		# シート名はASCII文字のみとする（Excelシート名の制限回避）。
		ws.title = "Report"

		# タイトル行
		ws.merge_cells("A1:E1")
		title_cell = ws["A1"]
		title_cell.value = excel_title
		title_cell.font = Font(size=16, bold=True)
		title_cell.alignment = Alignment(horizontal="center", vertical="center")

		# ヘッダー定義（DB取得項目 → Excel表示ラベル）
		fields = [
			("報告書番号", "報告書番号"),
			("都道府県連", "都道府県連"),
			("商工会", "商工会"),
			("実施日", "実施日"),
			("開始時刻", "開始時刻"),
			("終了時刻", "終了時刻"),
			("支援テーマ", "支援テーマ"),
			("業種", "業種"),
			("事業所名", "事業所名"),
			("担当者名", "担当者名"),
			("担当（主）", "担当（主）"),
			("担当（副）", "担当（副）"),
			("概要", "概要"),
			("内容", "内容"),
		]

		# ヘッダー行（3行目から）
		header_font = Font(bold=True)
		header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
		thin_border = Border(
			left=Side(style="thin"),
			right=Side(style="thin"),
			top=Side(style="thin"),
			bottom=Side(style="thin"),
		)

		for col_idx, (db_key, label) in enumerate(fields, 1):
			cell = ws.cell(row=3, column=col_idx, value=label)
			cell.font = header_font
			cell.fill = header_fill
			cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
			cell.border = thin_border

		# データ行（4行目）：取得データを各セルへ書き込む
		for col_idx, (db_key, label) in enumerate(fields, 1):
			val = utils.string_util.changeNullToBlank(str(row.get(db_key, "") or ""))
			if db_key == "実施日" and val:
				val = val[:10]
			cell = ws.cell(row=4, column=col_idx, value=val)
			cell.alignment = Alignment(vertical="top", wrap_text=True)
			cell.border = thin_border

		# 列幅調整
		col_widths = [14, 14, 22, 12, 10, 10, 24, 22, 22, 14, 14, 14, 30, 60]
		for i, w in enumerate(col_widths, 1):
			ws.column_dimensions[chr(64 + i)].width = w

		# 内容行の高さを広げる
		ws.row_dimensions[4].height = 120

		# 一時ファイルへ保存する（テンポラリファイル名はASCII英数字のみとする）。
		temp_dir = tempfile.gettempdir()
		report_code = utils.string_util.changeNullToBlank(row.get("報告書番号", ""))
		# 報告書番号の記号を置換してASCII安全なテンポラリファイル名を生成する。
		safe_code = report_code.replace("-", "").replace(" ", "_") or "temp"
		file_name = "formexport_" + safe_code + ".xlsx"
		file_path = os.path.join(temp_dir, file_name)
		wb.save(file_path)

		return file_path
