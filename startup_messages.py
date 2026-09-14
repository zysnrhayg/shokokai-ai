# py_startup_messages.vm - i18n messages for startup validation and health/ready endpoints (ja/zh/en)
# Generated - do not edit by hand; use generator to change.
"""
Startup and health check messages for i18n (ja, zh, en).
Used by config.validate_startup_config() and /health, /ready routes.
Locale selection: LANG/LC_ALL for console; Accept-Language or get_locale() for HTTP.
"""
import os

def _locale():
    """Current locale for console/startup (before Flask request context)."""
    return (os.getenv("LANG") or os.getenv("LC_ALL") or "en")[:2].lower() or "en"

# REQUIRED_ENV_MISSING: message when required env vars are missing. {names} = comma-separated list.
REQUIRED_ENV_MISSING = {
    "ja": "必須の環境変数が設定されていません: {names}",
    "zh": "缺少必需的环境变量: {names}",
    "en": "Missing required environment variable(s): {names}",
}

# HEALTH_OK: /health endpoint message
HEALTH_OK = {
    "ja": "OK",
    "zh": "正常",
    "en": "ok",
}

# READY_OK: /ready endpoint message when DB is reachable
READY_OK = {
    "ja": "準備完了",
    "zh": "就绪",
    "en": "ready",
}

# READY_DB_FAIL: /ready endpoint message when DB check fails
READY_DB_FAIL = {
    "ja": "データベース接続に失敗しました",
    "zh": "数据库连接失败",
    "en": "Database connection failed",
}

def get_required_env_missing(names):
    """Return REQUIRED_ENV_MISSING message for current locale."""
    loc = _locale()
    if loc not in REQUIRED_ENV_MISSING:
        loc = "en"
    return REQUIRED_ENV_MISSING[loc].format(names=names)

def get_health_ok():
    loc = _locale()
    return HEALTH_OK.get(loc, HEALTH_OK["en"])

def get_ready_ok():
    loc = _locale()
    return READY_OK.get(loc, READY_OK["en"])

def get_ready_db_fail():
    loc = _locale()
    return READY_DB_FAIL.get(loc, READY_DB_FAIL["en"])

def get_message_http(locale, key):
    """Get message for HTTP response by locale (e.g. from get_locale()). key: 'health_ok', 'ready_ok', 'ready_db_fail'."""
    if not locale:
        locale = "en"
    locale = locale[:2].lower() if len(locale) >= 2 else "en"
    if key == "health_ok":
        return HEALTH_OK.get(locale, HEALTH_OK["en"])
    if key == "ready_ok":
        return READY_OK.get(locale, READY_OK["en"])
    if key == "ready_db_fail":
        return READY_DB_FAIL.get(locale, READY_DB_FAIL["en"])
    return ""
