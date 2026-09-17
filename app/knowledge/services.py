# 顧客設計: app/knowledge/services.py
from types import SimpleNamespace
from app.dao.api154_getpublishedentries.api154_getpublishedentries_dao import (
    Api154GetpublishedentriesDao,
)
import utils.string_util


def _escape_ilike(keyword):
    """ILIKE の % / _ / ! をリテラルとして扱う（ESCAPE '!'）。"""
    return keyword.replace("!", "!!").replace("%", "!%").replace("_", "!_")


def _attach_theme_badges(rows):
    """顧客設計 SQL②の結果を各エントリの theme_badges に付与する。"""
    if not rows:
        return []
    dao = Api154GetpublishedentriesDao()
    theme_rows = dao.api154_getentrythemecodes(
        [r.get("knowledge_entry_id") for r in rows]
    )
    by_id = {}
    for t in theme_rows or []:
        eid = t.get("knowledge_entry_id")
        if eid is None:
            continue
        by_id.setdefault(eid, []).append(
            {
                "theme_id": t.get("theme_id"),
                "theme_code": t.get("theme_code") or "",
                "label": t.get("label") or "",
                "badge_class": t.get("badge_class") or "",
            }
        )
    for row in rows:
        eid = row.get("knowledge_entry_id")
        row["theme_badges"] = by_id.get(eid, [])
    return rows


def get_entries_with_themes(keyword="", prefecture_code=""):
    """公開中ナレッジとテーマバッジを取得する（AI相談① / ナレッジ検索で共用）。

    顧客設計どおり SQL①（一覧＋文書タイトル・県名）の後に SQL②（theme_code）を実行する。
    """
    kw = utils.string_util.changeNullToBlank(keyword)
    pref = utils.string_util.changeNullToBlank(prefecture_code)
    if not isinstance(kw, str):
        kw = "" if kw is None else str(kw)
    if not isinstance(pref, str):
        pref = "" if pref is None else str(pref)
    kw = kw[:80]
    if kw:
        kw = _escape_ilike(kw)
    q = SimpleNamespace(
        keyword=kw,
        prefecturecode=pref,
        prefecture_code=pref,
    )
    rows = Api154GetpublishedentriesDao().api154_getpublishedentries(q) or []
    return _attach_theme_badges(rows)
