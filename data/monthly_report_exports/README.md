# 帳票配布ディレクトリ（MONTHLY_REPORT_EXPORT_DIR）

## 本番
顧客アップロードの帳票ファイル（`report_*_template.xlsx` 等）をこのディレクトリ直下に置きます。
ファイル名は `cfg_excel_report_definition.template_filename` と一致させてください。

## テスト用ダミー
リポジトリには **1 ファイル**だけ同梱しています:

- `dummy_templates.zip`（中身: `dummy/report_h_template.xlsx` … `dummy/report_i8_template.xlsx`）

帳票出力時、直下に対象 xlsx が無い場合は zip から自動展開します。
展開された `*.xlsx` は `.gitignore` 対象です（コミット不要）。
