"""実績確認・帳票出力 ルート相当（顧客設計: app/monthly/routes.py）。

Flask では /monthlyexportapi.do が本モジュールの export_excel を呼び出す。
"""


def export_excel(session, dto):
    """
    帳票出力（設計書: export-excel）。
    cfg_excel_report_definition の VIEW 1行（または報単複数 slot）を取得し、
    cfg_excel_output_mapping に従ってテンプレートへ書き込む。

    Returns (abs_path, download_filename, form_code, fiscal_year_code).
    """
    from app.common.excel_export import render_aggregate_excel

    return render_aggregate_excel(session, dto)
