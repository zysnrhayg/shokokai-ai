# 顧客設計: app/common/menu.py
"""ロール別メニュー（cfg_menu_item）。プロセス内キャッシュあり。"""
import threading
import time

import utils.mysqldb_utils as db
import utils.string_util

_visible_menu_cache = {}
_cache_lock = threading.Lock()
_CACHE_TTL_SEC = 60

FE_ROLE_TO_MENU = {
    "national": "zenkoku",
    "pref": "ken",
    "shokokai": "shokokai",
}

# cfg_menu_item.screen_id → フロントの hash route
SCREEN_TO_ROUTE = {
    "dashboard": "home",
    "home": "home",
    "ai-input": "ai-input",
    "manual-input": "manual-input",
    "expert-import": "expert-import",
    "reports": "reports",
    "monthly": "monthly",
    "accounts": "accounts",
    "knowledge": "knowledge",
    "ai-proposal": "ai-proposal",
}


def _blank(v):
    return utils.string_util.changeNullToBlank(v)


def clear_menu_cache():
    with _cache_lock:
        _visible_menu_cache.clear()


def get_visible_menu(role_code=""):
    """顧客設計: SELECT * FROM cfg_menu_item WHERE role_code = %s ORDER BY ..."""
    fe = _blank(role_code) or "shokokai"
    db_role = FE_ROLE_TO_MENU.get(fe, fe)
    now = time.time()
    with _cache_lock:
        hit = _visible_menu_cache.get(db_role)
        if hit and (now - hit[0]) < _CACHE_TTL_SEC:
            return list(hit[1])

    rows = db.result_to_list_of_dict(
        db.querySQL(
            """
SELECT role_code
     , section_sort_order
     , sort_order
     , section_label
     , label
     , icon
     , screen_id
     , default_form
     , requires_capability
     , subtitle
FROM cfg_menu_item
WHERE role_code = :role_code
  AND deleted_at IS NULL
ORDER BY section_sort_order, sort_order
""",
            {"role_code": db_role},
        )
    ) or []

    out = []
    for r in rows:
        screen = _blank(r.get("screen_id"))
        default_form = _blank(r.get("default_form"))
        route = SCREEN_TO_ROUTE.get(screen, screen)
        # ナレッジ検索は同一 screen_id=ai-proposal + default_form=search
        if screen == "ai-proposal" and default_form == "search":
            route = "knowledge-search"
        out.append(
            {
                "role_code": _blank(r.get("role_code")),
                "section_sort_order": r.get("section_sort_order"),
                "sort_order": r.get("sort_order"),
                "section_label": _blank(r.get("section_label")),
                "label": _blank(r.get("label")),
                "icon": _blank(r.get("icon")),
                "screen_id": screen,
                "default_form": default_form,
                "requires_capability": _blank(r.get("requires_capability")),
                "subtitle": _blank(r.get("subtitle")),
                "route": route,
            }
        )

    with _cache_lock:
        _visible_menu_cache[db_role] = (now, list(out))
    return out
