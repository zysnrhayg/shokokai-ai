# -*- coding: utf-8 -*-
"""報告書を見る（顧客設計: app/reports/services.py）。"""
from flask import session

import utils.mysqldb_utils as db
import utils.string_util
from app.common.api_json import jsonable_row


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def _q(sql, params=None):
    return db.result_to_list_of_dict(db.querySQL(sql, params or {})) or []


def resolve_role_scope(rolecode=None):
    """
    WHERE はロールにより変わる（顧客設計）:
      - 全国: 絞りなし
      - 県連: prefecture_code のみ
      - 商工会: prefecture_code + shokokai_cd
    """
    role = _blank(rolecode) or "shokokai"
    sess_pref = _blank(session.get("PREFECTURE_CODE"))
    sess_sho = _blank(session.get("SHOKOKAI_CD"))
    if sess_pref == "00" and role == "shokokai":
        role = "national"
    pref = ""
    sho = ""
    if role == "shokokai":
        pref = sess_pref
        sho = sess_sho
        if pref == "00":
            pref = ""
            sho = ""
            role = "national"
    elif role == "pref":
        pref = sess_pref
        if pref == "00":
            pref = ""
            role = "national"
    return {"role": role, "prefecture_code": pref, "shokokai_cd": sho}


def get_visible_reports(rolecode=None, limit=None, offset=None):
    """
    ① 一覧テーブル取得（顧客設計 SQL・ロール範囲のみ）。
    画面条件での絞込は reports_api.fetch_reports（サーバ側）で実施。
    """
    scope = resolve_role_scope(rolecode)
    params = {
        "prefecture_code": scope["prefecture_code"],
        "shokokai_cd": scope["shokokai_cd"],
    }
    # 顧客提供 SQL に準拠（JOIN 種別・列・ORDER BY）
    sql = """
SELECT trn_report.report_id
     , trn_report.report_code
     , mst_industry.label AS industry
     , trn_report.report_date
     , trn_report.summary
     , trn_report.staff_main_name
     , trn_report.staff_sub_name
     , trn_report.registered_at
     , trn_report.status
     , trn_report.printed_at
     , trn_report.prefecture_code
     , trn_report.shokokai_cd
     , mst_prefecture.name AS prefecture_name
     , mst_shokokai.name AS shokokai_name
     , mst_theme.theme_code
     , mst_theme.label AS theme_label
     , mst_theme.badge_class AS theme_badge_class
     , trn_report.form_code
     , mst_form.short_label AS form_short_label
     , mst_form.badge_class AS form_badge_class
FROM trn_report
JOIN mst_prefecture
  ON mst_prefecture.prefecture_code = trn_report.prefecture_code
JOIN mst_shokokai
  ON mst_shokokai.prefecture_code = trn_report.prefecture_code
 AND mst_shokokai.shokokai_cd = trn_report.shokokai_cd
LEFT JOIN mst_theme
  ON mst_theme.theme_id = trn_report.theme_id
LEFT JOIN mst_form
  ON mst_form.form_code = trn_report.form_code
 AND mst_form.fiscal_year_id = trn_report.fiscal_year_id
LEFT JOIN mst_industry
  ON mst_industry.industry_code = trn_report.industry_code
 AND mst_industry.fiscal_year_id = trn_report.fiscal_year_id
WHERE COALESCE(trn_report.status, '') <> '削除'
  AND trn_report.deleted_at IS NULL
"""
    if params["prefecture_code"]:
        sql += "  AND trn_report.prefecture_code = :prefecture_code\n"
    if params["shokokai_cd"]:
        sql += "  AND trn_report.shokokai_cd = :shokokai_cd\n"
    sql += "ORDER BY trn_report.report_date DESC, trn_report.registered_at DESC"
    if limit is not None:
        params["limit"] = int(limit)
        params["offset"] = int(offset or 0)
        sql += "\nLIMIT :limit OFFSET :offset"
    return [jsonable_row(rec) for rec in _q(sql, params)]
