# account list row mapping for AccountsInitAPI / AccountsFilterAPI dragB
from datetime import datetime

def _blank(v):
    if v is None:
        return ""
    return str(v)

def _format_last_login(v):
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.strftime("%Y/%m/%d %H:%M:%S")
    s = str(v).strip()
    return s or None

def _qualification_codes(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v]
    s = str(v).strip()
    if not s or s == "{}":
        return []
    # PostgreSQL array text like {a,b}
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1]
        if not inner:
            return []
        return [p.strip().strip('"') for p in inner.split(",") if p.strip()]
    return [s]

def account_row_to_selmap(entity):
    """Map a DB row (dict) to the frontend account list shape."""
    if entity is None:
        return {}
    get = entity.get if hasattr(entity, "get") else lambda k, d=None: getattr(entity, k, d)
    status_raw = get("status")
    try:
        status = int(status_raw) if status_raw is not None and status_raw != "" else 0
    except (TypeError, ValueError):
        status = 0
    core = get("core_linked")
    return {
        "user_account_id": get("user_account_id"),
        "prefecture_code": _blank(get("prefecture_code")),
        "shokokai_cd": _blank(get("shokokai_cd")),
        "user_id": _blank(get("user_id")),
        "shokuin_kj": _blank(get("shokuin_kj")),
        "email": _blank(get("email")),
        "status": status,
        "core_linked": bool(core) if core is not None else False,
        "permission_level": _blank(get("permission_level")),
        "last_login_at": _format_last_login(get("last_login_at")),
        "prefecture_name": _blank(get("prefecture_name")),
        "shokokai_name": _blank(get("shokokai_name")),
        "qualification_codes": _qualification_codes(get("qualification_codes")),
    }
