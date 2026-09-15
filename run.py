"""Flask Web サイトの起動処理。"""
#run.py
# py_root_run.vm はアプリケーションとルーティングを生成する。
# config が run.py と同じディレクトリの settings.toml を読むよう、先にルートを確定する。
import os
_run_dir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
os.environ.setdefault("PROJECT_ROOT", _run_dir)
os.chdir(_run_dir)

from dotenv import load_dotenv
load_dotenv()

# Import necessary modules and libraries
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask import Response,jsonify,Flask,redirect,url_for,request,flash,session
from flask import render_template, g, request  # Used for template rendering and request handling
from dynaconf import FlaskDynaconf  # Used to load configurations
from werkzeug.exceptions import HTTPException  # Used to handle HTTP exceptions
import jsonpickle
from functools import wraps
import utils.session_constant
from requests import RequestException
# 共通設定を読み込み、アプリケーション生成前に必須設定と本番安全設定を検証する。
from config import (
    settings,
    get_database_uri,
    DB_USER,
    DB_DRIVER,
    validate_startup_config,
    validate_production_security,
)
validate_startup_config()
validate_production_security()
from exts import (
    app,
    db,
    mail,
    migrate,
    babel,
)  # Import custom Flask extensions
from utils import log_exception
from utils import csrf_protect
csrf_protect.init_csrf(app)
from app.controller import logincontroller
from app.controller import commonfunctioncontroller
import utils.config
import utils.mysqldb_utils
from utils.jsonwfc_object import JSONWFCObject
import utils.json_constant
try:
    from utils.message_util import getMessageById
except ImportError:
    import resources.messages as _res_msg
    def getMessageById(msgid):
        return _res_msg.getMessageById(msgid)
import initdatabase_postgres
from flask import session
from app.controller.m001 import m001_controller
# Log the application startup information
# - logger.info() records an info level log message
# - "App is running..." indicates that the application is running
utils.config.global_log.info("The application is running...")
# Database connection is established at startup; restart the app after changing settings.toml for changes to take effect
utils.config.global_log.info(
    "Database driver=%s user=%s (restart required after changing settings.toml)"
    % (DB_DRIVER, DB_USER or "(default)")
)

# load_dotenv() already called at top of file


def get_locale():
    """Automatically detect the current language"""

    # If the user is logged in, use the user's preferred language
    # Use `getattr(g, "user", None)` to get the user object
    user = getattr(g, "user", None)
    if user is not None:
        # If the user object exists and has a language property (e.g., `user.locale`), use the user's preferred language.
        locale = getattr(user, "locale", None)
        if locale:
            utils.config.global_log.info(f"Language from user settings: {locale}")
            return locale
    # Otherwise, try to infer the best language from the browser headers
    locale = request.accept_languages.best_match(["ja", "zh", "en"])
    utils.config.global_log.info(f"Language from browser settings: {locale}")
    return locale


# Create the instance directory and store the instantiated application data
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# 対象 DB が無ければ作成し、ddl_define.sql でテーブルを投入する。
if (DB_DRIVER or "").lower() in ("postgresql", "postgres", "pgsql"):
    try:
        _pg_init = initdatabase_postgres.ensure_database()
        utils.config.global_log.info("PostgreSQL database init: %s", _pg_init)
    except Exception as _pg_err:
        utils.config.global_log.warning("PostgreSQL database init failed: %s", _pg_err)
# DB init: only when RUN_DB_INIT=true at runtime. Production: run DB init via separate script/CI, not on app startup.
if os.getenv("RUN_DB_INIT", "false").lower() == "true":
    import initdatabase_mysql
    initdatabase_mysql.installDb()
# Initialize each plugin
dynaconf = FlaskDynaconf(app, dynaconf_instance=settings)  # Load settings with Dynaconf
# settings.toml の空 SECRET_KEY で上書きされないよう、環境変数を優先する
_secret_key = (os.environ.get("SECRET_KEY") or app.secret_key or "").strip()
if _secret_key:
    app.secret_key = _secret_key
    app.config["SECRET_KEY"] = _secret_key
babel.init_app(app, default_locale="ja")  # Initialize internationalization and localization
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
# Validate DB connection at startup to avoid Unknown database errors only when logging in or querying
_ok, _err = utils.mysqldb_utils.check_connection()
if not _ok:
    utils.config.global_log.warning("Database connection check failed at startup: %s (fix DB_NAME in settings.toml or create the database)" % (_err or "unknown"))
else:
    utils.config.global_log.info("Database connection check OK")
app.register_blueprint(m001_controller.m001_route)
app.register_blueprint(logincontroller.login_route)
app.register_blueprint(commonfunctioncontroller.commonfunction_route)
db.init_app(app)  # Initialize the database
mail.init_app(app)  # Initialize the mail extension
migrate.init_app(app, db)
login_manager = LoginManager()
#login_manager.init_app(app)

@app.route("/health")
def health():
    """Liveness: app is up. Message is i18n via startup_messages."""
    from startup_messages import get_message_http
    _loc = request.accept_languages.best_match(["ja", "zh", "en"]) or "en"
    return jsonify({"status": "ok", "message": get_message_http(_loc, "health_ok")}), 200

@app.route("/ready")
def ready():
    """Readiness: app and DB are ready. Returns 503 if DB check fails; message is i18n."""
    from startup_messages import get_message_http
    _loc = request.accept_languages.best_match(["ja", "zh", "en"]) or "en"
    ok, _err = utils.mysqldb_utils.check_connection()
    if ok:
        return jsonify({"status": "ok", "message": get_message_http(_loc, "ready_ok")}), 200
    return jsonify({"status": "unavailable", "message": get_message_http(_loc, "ready_db_fail")}), 503

@app.before_request
def session_interceptor():
    if request.path.startswith('/static'):
        return None
    ok, out = csrf_protect.check_csrf(app, request, session, getMessageById)
    if not ok:
        return out[0], out[1]
    allowed_routes = [
        'login_route.pythonLogin',
        '/',
        'index',
        'commonfunction_route.logininitapi',
        'commonfunction_route.loginapi',
        'commonfunction_route.verify2faapi',
    ]
    if request.endpoint != None :
        if request.endpoint not in allowed_routes and 'APP_USER_ID' not in session:
            if request.path.endswith('.do') == False:
                return None
            jsonObj = JSONWFCObject()
            try:
                _timeout_msg = getMessageById("msg_session_timeout")
            except Exception:
                try:
                    import resources.messages as _res_msg
                    _timeout_msg = _res_msg.getMessageById("msg_session_timeout")
                except Exception:
                    _timeout_msg = "msg_session_timeout"
            if _timeout_msg == "msg_session_timeout":
                try:
                    import resources.messages as _res_msg
                    _timeout_msg = _res_msg.getMessageById("msg_session_timeout")
                except Exception:
                    pass
            _timeout_msg = _timeout_msg.replace("'", "\\'")
            jsonObj.setScript(utils.json_constant.JSONID_RUN_SCRIPT, "alert('" + _timeout_msg + "');")
            jsonObj.setScript(utils.json_constant.JSONID_RUN_SCRIPT, "location.href='./'")
            return jsonObj.toJsonString()

_MONTHLY_DATA_PATH = os.path.join(_run_dir, "static", "mockup", "data", "monthly-data.json")

def _load_monthly_data():
    try:
        with open(_MONTHLY_DATA_PATH, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return "{}"

def render_frontend():
    """Render the mockup SPA (login + app shell)."""
    logged_in = bool(session.get(utils.session_constant.USER_ID) or session.get("APP_USER_ID"))
    return render_template(
        "app.html",
        monthly_data=_load_monthly_data(),
        logged_in=logged_in,
        csrf_token=csrf_protect.get_csrf_token(session),
    )

@app.route("/")
def index():
    """Homepage of the website"""
    return render_frontend()

@app.route("/favicon.ico")
def favicon():
    return "", 204

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(utils.session_constant.USER_ID,'') == '':
           return render_frontend()
        return func(*args, **kwargs)
    return wrapper


@app.route("/error/500")
def error_500():
    """Demonstrate a 500 error"""
    1 / 0  # Trigger a zero division error to cause a 500 error

@app.route("/logout")
def logout():
   session[utils.session_constant.USER_ID] = ""
   session.pop("APP_USER_ID", None)
   session.pop("LOGIN_USER_ID", None)
   return redirect(url_for("index"))

@app.route("/error/400")
def error_400():
    """Demonstrate a 400 error"""
    from werkzeug.exceptions import HTTPException

    raise HTTPException()


@app.route("/error/params")
def error_params():
    """Custom error"""


    # Trigger a custom parameter error
    raise RequestException("Request params error")


@app.errorhandler(Exception)
def handle_500_exception(e):
    """Decorator: Handle 500 errors. In production, do not return str(e) or traceback."""
    log_exception(e)
    if isinstance(e, HTTPException):
        return e
    is_production = os.getenv("FLASK_ENV", "production").lower() != "development"
    if is_production:
        try:
            msg = getMessageById("error_internal")
        except Exception:
            msg = "Internal server error"
        return jsonify({"e": msg, "message": msg}), 500
    return jsonify({"e": str(e), "message": str(e)}), 500


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Decorator: Handle HTTP exceptions. In production, do not return internal details."""
    log_exception(e)
    is_production = os.getenv("FLASK_ENV", "production").lower() != "development"
    if is_production:
        try:
            msg = getMessageById("error_operation_failed")
        except Exception:
            msg = "Operation failed"
        return jsonify({"e": msg, "message": msg}), e.code
    return e.get_response()

if __name__ == '__main__':
    # host/port/debug from env; production: use gunicorn e.g. gunicorn -w 4 -b 0.0.0.0:5000 run:app
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_ENV", "production").lower() == "development"
    app.run(host=host, port=port, debug=debug)
