# 顧客設計: app/knowledge/services.py
from types import SimpleNamespace
from app.dao.api154_getpublishedentries.api154_getpublishedentries_dao import (
    Api154GetpublishedentriesDao,
)
import utils.string_util


def _escape_ilike(keyword):
    """ILIKE の % / _ / ! をリテラルとして扱う（ESCAPE '!'）。"""
    return keyword.replace("!", "!!").replace("%", "!%").replace("_", "!_")


def get_entries_with_themes(keyword="", prefecture_code=""):
    """公開中ナレッジとテーマバッジを取得する（AI相談① / ナレッジ検索で共用）。"""
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
    return Api154GetpublishedentriesDao().api154_getpublishedentries(q) or []
