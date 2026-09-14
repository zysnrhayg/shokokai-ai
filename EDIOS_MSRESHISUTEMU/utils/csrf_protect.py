# csrf_protect.py
# py_csrf.vm - CSRF token-based protection. Exempt paths: login, health, ready (configurable via CSRF_EXEMPT_PATHS).
import os
import secrets

def _normalize_path(p):
    p = (p or "").strip()
    if not p.startswith("/"):
        p = "/" + p
    if len(p) > 1 and p.endswith("/"):
        p = p.rstrip("/")
    return p

def _exempt_paths():
    # Keep default exemptions minimal and explicit.
    raw = os.getenv("CSRF_EXEMPT_PATHS", "/login.do,/health,/ready")
    paths = [_normalize_path(p) for p in raw.split(",") if p.strip()]
    # Never allow global exemption via "/".
    return [p for p in paths if p != "/"]

def _is_exempt_path(path, exempt):
    # Exact match for endpoint exemption.
    if path == exempt:
        return True
    # Prefix exemption for grouped APIs, but never for root.
    return exempt != "/" and path.startswith(exempt + "/")

def init_csrf(app):
    """Set CSRF_ENABLED from settings/env (default False). Call once after app settings are loaded."""
    raw = app.config.get("CSRF_ENABLED", os.getenv("CSRF_ENABLED", "false"))
    if isinstance(raw, bool):
        app.config["CSRF_ENABLED"] = raw
        return
    app.config["CSRF_ENABLED"] = str(raw).lower() in ("1", "true", "yes", "on")

def ensure_csrf_token_in_session(session):
    """Ensure session has a csrf_token; create if missing."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(24)

def get_csrf_token(session):
    """Return current CSRF token for the session (for embedding in forms or returning to client)."""
    ensure_csrf_token_in_session(session)
    return session["csrf_token"]

def check_csrf(app, request, session, get_message_by_id):
    """
    Validate CSRF for state-changing methods. Returns (True, None) if valid or exempt,
    or (False, response) to return 403 with i18n message.
    """
    if not app.config.get("CSRF_ENABLED", True):
        return True, None
    if request.method not in ("POST", "PUT", "DELETE", "PATCH"):
        return True, None
    path = _normalize_path(request.path or "")
    for exempt in _exempt_paths():
        if _is_exempt_path(path, exempt):
            return True, None
    ensure_csrf_token_in_session(session)
    token_from_request = request.headers.get("X-CSRFToken") or request.form.get("csrf_token") or (request.get_json(silent=True) or {}).get("csrf_token")
    if not token_from_request or not secrets.compare_digest(token_from_request, session.get("csrf_token", "")):
        try:
            msg = get_message_by_id("error_csrf_invalid")
        except Exception:
            msg = "CSRF validation failed"
        from flask import jsonify
        return False, (jsonify({"e": msg, "status": "error", "message": msg}), 403)
    return True, None
