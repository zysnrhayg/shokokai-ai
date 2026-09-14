#logger.py
#py_root_logger.vm make logger template
#
# パスワード、トークン、カード番号などの機密情報をログへ出力しない。
# 機微項目を記録する必要がある場合は、事前にマスキングする。
# request_id と user_id は追跡専用とし、機密情報を設定しない。
#
# PROJECT_ROOT は環境変数を優先し、未指定時は本ファイルの配置先をプロジェクトルートとする。
import os
from logging import Logger, getLogger, FileHandler, StreamHandler, Formatter, Filter, LoggerAdapter
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
import utils.session_constant

# リクエスト外でもログを利用できるよう Flask コンテキストを条件付きで参照する。
try:
    from flask import has_app_context, g, request, session
except ImportError:
    has_app_context = lambda: False
    g = request = session = None


class RequestContextFilter(Filter):
    """追跡用 request_id と user_id をログレコードへ設定する。"""

    def filter(self, record):
        if has_app_context():
            record.request_id = getattr(g, 'request_id', '-')
            try:
                record.user_id = (session.get(utils.session_constant.USER_ID, '') or '-') if session else '-'
            except Exception:
                record.user_id = '-'
        else:
            record.request_id = getattr(record, 'request_id', '-')
            record.user_id = getattr(record, 'user_id', '-')
        return True


class NoNewlineMessageFilter(Filter):
    """ログ一件を一行に保つため、メッセージ内の改行を空白へ変換する。"""

    def filter(self, record):
        if getattr(record, 'msg', None) and isinstance(record.msg, str) and '\n' in record.msg:
            record.msg = record.msg.replace('\n', ' ').replace('\r', ' ')
        if getattr(record, 'message', None) and isinstance(record.message, str) and '\n' in record.message:
            record.message = record.message.replace('\n', ' ').replace('\r', ' ')
        return True


class VerboseFormatter(Formatter):
    """追跡項目を補完し、整形後のログを一行へ正規化する。"""

    def format(self, record):
        setattr(record, 'request_id', getattr(record, 'request_id', '-'))
        setattr(record, 'user_id', getattr(record, 'user_id', '-'))
        s = super().format(record)
        if '\n' in s or '\r' in s:
            s = s.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        return s


class Log(object):
    """プロジェクトルート配下へローテーションログを出力する。"""

    # 本 logger.py が配置されたディレクトリ。
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 本テンプレートはプロジェクト直下の logger.py を生成するため、配置先自体が既定ルートとなる。
    _default_root = current_dir
    project_root = os.getenv('PROJECT_ROOT', _default_root)
    if not os.path.isabs(project_root):
        project_root = os.path.abspath(os.path.join(current_dir, project_root))

    # 共通ログの出力先。
    LOG_PATH = os.path.join(project_root, "log")
    # 利用者別ログの出力先。
    USER_LOG_PATH = os.path.join(project_root, "log", "sift")

    # 一ファイル 10 MB、バックアップ 10 世代でローテーションする。
    LOG_MAX_BYTES = 10 * 1024 * 1024
    LOG_BACKUP_COUNT = 10

    @classmethod
    def init(cls, user=None):
        """ログ出力先とハンドラーを初期化する。"""

        if not os.path.exists(cls.LOG_PATH):
            os.makedirs(cls.LOG_PATH)
        if not os.path.exists(cls.USER_LOG_PATH):
            os.makedirs(cls.USER_LOG_PATH)

        # Log level: APP_LOG_LEVEL env; if unset, DEBUG for development else INFO
        env_name = os.getenv("FLASK_ENV", os.getenv("ENV", "production"))
        default_level = "DEBUG" if (env_name and env_name.lower() == "development") else "INFO"
        logger_level = os.getenv("APP_LOG_LEVEL", default_level)

        loggers_sets = ["console", "debug_file", "info_file"]

        # Format: include request_id, user_id, module for tracing
        log_format = (
            '%(asctime)s %(levelname)s %(name)s %(process)d %(request_id)s %(user_id)s %(module)s '
            '%(filename)s %(funcName)s %(lineno)d %(message)s'
        )

        handlers_sets = {
            "console": {
                "formatter": "verbose",
                "level": logger_level,
                "class": "logging.StreamHandler"
            },
            "debug_file": {
                "formatter": "verbose",
                "level": logger_level,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(cls.LOG_PATH, "python_debug.log"),
                "mode": "a",
                "maxBytes": cls.LOG_MAX_BYTES,
                "backupCount": cls.LOG_BACKUP_COUNT,
                "encoding": "utf-8"
            },
            "info_file": {
                "formatter": "verbose",
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(cls.LOG_PATH, "python_info.log"),
                "mode": "a",
                "maxBytes": cls.LOG_MAX_BYTES,
                "backupCount": cls.LOG_BACKUP_COUNT,
                "encoding": "utf-8"
            }
        }

        log_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    '()': __name__ + '.VerboseFormatter',
                    'format': log_format
                }
            },
            'handlers': handlers_sets,
            'loggers': {
                '': {
                    'handlers': loggers_sets,
                    'level': logger_level,
                }
            }
        }

        # User-specific log: RotatingFileHandler per user
        if user and user != 'unknown_user':
            for level in ("debug", "info"):
                filename = os.path.join(cls.USER_LOG_PATH, f"{user}_{level}.log")
                key = f"user_{level}_file"
                handlers_sets[key] = {
                    "formatter": "verbose",
                    "level": level.upper(),
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": filename,
                    "mode": "a",
                    "maxBytes": cls.LOG_MAX_BYTES,
                    "backupCount": cls.LOG_BACKUP_COUNT,
                    "encoding": "utf-8"
                }
                log_config['loggers']['']['handlers'].append(key)

        dictConfig(log_config)

        # Inject request_id/user_id into every record (set in run.py before_request: g.request_id)
        root = getLogger()
        if not any(isinstance(f, RequestContextFilter) for f in root.filters):
            root.addFilter(RequestContextFilter())
        if not any(isinstance(f, NoNewlineMessageFilter) for f in root.filters):
            root.addFilter(NoNewlineMessageFilter())

    @classmethod
    def getLog(cls, user: str = "unknown_user") -> Logger:
        """Get logger. Optional user for user-scoped file handlers.
        Args:
            user (str): User identifier for sift logs.
        Returns:
            Logger: Logger instance or LoggerAdapter with user in extra.
        """
        Log.init(user)
        logger = getLogger(__name__)
        if user == 'unknown_user':
            return logger
        return LoggerAdapter(logger, {"user": user})


def silence_sqlalchemy_builtin_sql_logs() -> None:
    """When SQL_ECHO is on, suppress sqlalchemy built-in SQL logs (custom handler in mysqldb_utils logs instead)."""
    import logging

    try:
        from config import SQL_ECHO as _sql_echo_cfg
        sql_echo_on = str(_sql_echo_cfg or "").lower() == "true"
    except Exception:
        sql_echo_on = os.getenv("SQL_ECHO", "false").lower() == "true"
    if not sql_echo_on:
        return
    sa_names = {"sqlalchemy", "sqlalchemy.engine", "sqlalchemy.pool", "sqlalchemy.dialects"}
    for name in list(getLogger().manager.loggerDict.keys()):
        if name.startswith("sqlalchemy"):
            sa_names.add(name)
    for name in sorted(sa_names):
        sa_log = getLogger(name)
        sa_log.handlers.clear()
        sa_log.propagate = False
        sa_log.setLevel(logging.WARNING)


currentLog = Log()


class LoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['user'], msg), kwargs
