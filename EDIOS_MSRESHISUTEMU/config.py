# Dynaconf を使用してアプリケーション設定を管理する。
# DB 設定は PROJECT_ROOT 配下の settings.toml または環境変数から取得する。

import os
import sys
from urllib.parse import quote_plus

from dynaconf import Dynaconf

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# プロジェクトルートは run.py が設定する環境変数を優先する。
_root = os.environ.get("PROJECT_ROOT") or os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
_settings_toml_path = os.path.join(_root, "settings.toml")

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    environments=True,
    root_path=_root,
    settings_files=[_settings_toml_path],
)

# PROJECT_ROOT で決定した settings.toml を TOML パーサーで直接読み込む。
def _load_db_from_toml():
    path = os.environ.get("SETTINGS_TOML_PATH") or _settings_toml_path
    path = os.path.abspath(os.path.realpath(path))
    if not os.path.isfile(path):
        print(f"[Config] WARN: settings.toml が見つかりません: {path}", flush=True)
        return {}
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        out = dict(data.get("default") or {})
        env_name = (os.getenv("FLASK_ENV") or os.getenv("ENV_FOR_DYNACONF") or "default").strip().lower()
        if env_name and env_name != "default":
            overlay = data.get(env_name)
            if isinstance(overlay, dict):
                out.update(overlay)
        print(
            f"[Config] 設定を読み込みました: {path} | env={env_name} "
            f"DB_NAME={out.get('DB_NAME')} DB_USER={out.get('DB_USER')} DB_PORT={out.get('DB_PORT')}",
            flush=True,
        )
        return out
    except (OSError, tomllib.TOMLDecodeError) as error:
        print(f"[Config] ERROR: 設定を読み込めませんでした: {path}: {error}", flush=True)
        raise

_toml_defaults = _load_db_from_toml()

def _get(key: str, default: str = None):
    v = os.getenv(key)
    if v is not None and v != "":
        return v
    v = _toml_defaults.get(key)
    if v is not None and v != "":
        return str(v)
    return default


def _normalize_db_driver(raw) -> str:
    """本プロジェクトの DB ドライバーを PostgreSQL に統一する。"""
    if raw is None or str(raw).strip() == "":
        return "postgresql"
    s = str(raw).strip().lower()
    if s in ("postgresql", "postgres", "pgsql"):
        return "postgresql"
    print(f"[Config] WARN: DB_DRIVER={raw!r} は使用せず PostgreSQL を使用します。", flush=True)
    return "postgresql"


DB_DRIVER = _normalize_db_driver(_get("DB_DRIVER"))


def get_database_uri():
    uri = _get("DATABASE_URI") or _toml_defaults.get("SQLALCHEMY_DATABASE_URI") or _toml_defaults.get("DATABASE_URI")
    if uri:
        return str(uri)
    host = _get("DB_HOST")
    port = _get("DB_PORT")
    user = _get("DB_USER")
    password = _get("DB_PASSWORD")
    db_name = _get("DB_NAME")
    if not all((host, port, user, password, db_name)):
        return None
    u = quote_plus(user)
    p = quote_plus(password)
    return f"postgresql+psycopg://{u}:{p}@{host}:{port}/{db_name}"

# run.py と共通処理が同じ設定値を参照できるよう DB 設定を公開する。
SQLALCHEMY_DATABASE_URI = get_database_uri()
DB_HOST = _get("DB_HOST")
DB_PORT = _get("DB_PORT")
DB_USER = _get("DB_USER")
DB_PASSWORD = _get("DB_PASSWORD")
DB_NAME = _get("DB_NAME")

# SQL ログ設定は settings.toml または環境変数から取得する。
SQL_ECHO = _get("SQL_ECHO", "false")
SQL_LOG_MAX_LEN = int(_get("SQL_LOG_MAX_LEN", "800") or "800")


def _coerce_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in ("true", "1", "yes", "on")


def get_bool_setting(key: str, default: bool = False, *, prefer_env: bool = True) -> bool:
    """
    settings.toml と指定時の環境変数から真偽値を取得する。
    prefer_env=True の場合は環境変数を優先する。
    """
    v = settings.get(key, None)
    if v is not None and str(v).strip() != "":
        return _coerce_bool(v)
    if prefer_env:
        raw = os.getenv(key)
        if raw is not None and str(raw).strip() != "":
            return _coerce_bool(raw)
    return default

# 起動時に SECRET_KEY と DB 接続先が必要となる。
REQUIRED_ENV_KEYS = ["SECRET_KEY"]

# 本番環境では使用を禁止する既知の開発用秘密鍵。
_WEAK_SECRET_KEYS = frozenset(
    {
        "dev-secret-key-change-in-production",
        "change-me",
        "secret",
        "changeme",
    }
)


def _is_production_env() -> bool:
    env = (os.getenv("FLASK_ENV") or os.getenv("ENV_FOR_DYNACONF") or "").strip().lower()
    return env == "production"


def _bool_env_first(key: str, default: bool = False) -> bool:
    """セキュリティ項目はプロセス環境変数を優先して取得する。"""
    raw = os.getenv(key)
    if raw is not None and str(raw).strip() != "":
        return _coerce_bool(raw)
    return get_bool_setting(key, default, prefer_env=False)


def get_session_timeout_minutes() -> int:
    """
    セッション有効時間（分）。settings.toml の SESSION_TIMEOUT_MINUTES のみ参照。
    0 または未設定 = タイムアウトなし（脆弱性診断中など）。
    製品版は 30 を設定する。
    """
    raw = _toml_defaults.get("SESSION_TIMEOUT_MINUTES", 0)
    try:
        minutes = int(str(raw).strip())
    except (TypeError, ValueError):
        return 0
    return minutes if minutes > 0 else 0


def collect_production_security_issues():
    """本番起動を禁止するセキュリティ設定不備を返す。"""
    if not _is_production_env():
        return []
    issues = []
    if not _bool_env_first("CSRF_ENABLED", False):
        issues.append(
            "本番環境では CSRF_ENABLED=true を設定してください。"
        )
    cors = (_get("CORS_ORIGINS") or "").strip()
    if not cors or cors == "*":
        issues.append(
            "本番環境の CORS_ORIGINS には明示的な許可元を設定してください。"
        )
    secret = (_get("SECRET_KEY") or "").strip()
    if not secret or secret in _WEAK_SECRET_KEYS or len(secret) < 16:
        issues.append(
            "SECRET_KEY が未設定、16文字未満、または既知の開発用値です。"
        )
    return issues


def collect_production_security_warnings():
    """本番環境の警告対象設定を返す。"""
    if not _is_production_env():
        return []
    warnings = []
    if _bool_env_first("SQL_ECHO", False):
        warnings.append(
            "本番環境の SQL_ECHO=true は機密 SQL を記録するため、false にしてください。"
        )
    return warnings


def validate_production_security():
    """本番セキュリティ基準を検証し、不備がある場合は終了コード 1 で停止する。"""
    import sys

    for w in collect_production_security_warnings():
        print(f"[Config] WARN: {w}", flush=True)
    issues = collect_production_security_issues()
    if not issues:
        return
    print(
        "[Config] ERROR: 本番セキュリティ設定の検証に失敗しました:\n  - "
        + "\n  - ".join(issues),
        flush=True,
    )
    sys.exit(1)


def validate_startup_config():
    """起動必須設定を検証し、不足時は終了コード1で停止する。"""
    import sys
    import startup_messages

    missing = []
    if not _get("SECRET_KEY"):
        missing.append("SECRET_KEY")
    uri = get_database_uri()
    if not uri:
        missing.append(
            "DATABASE_URI または DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME"
        )
    if not missing:
        return
    msg = startup_messages.get_required_env_missing(", ".join(missing))
    print(msg, flush=True)
    sys.exit(1)
