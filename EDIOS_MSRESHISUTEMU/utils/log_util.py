# log_util.py
# py_util_log.vm make log util template
# PROJECT_ROOT: override by env PROJECT_ROOT; default: two levels above this file.
import os
from logging import Logger, getLogger, FileHandler, StreamHandler, Formatter, Filter, LoggerAdapter
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
import utils.session_constant

# Optional: safe import for request context (Filter may run outside request)
try:
    from flask import has_app_context, g, request, session
except ImportError:
    has_app_context = lambda: False
    g = request = session = None


class RequestContextFilter(Filter):
    """Inject request_id, user_id into LogRecord for tracing. Attached to root logger after dictConfig."""

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


class VerboseFormatter(Formatter):
    """Formatter that ensures request_id and user_id exist on record before formatting (avoids KeyError when filter not in chain)."""

    def format(self, record):
        setattr(record, 'request_id', getattr(record, 'request_id', '-'))
        setattr(record, 'user_id', getattr(record, 'user_id', '-'))
        return super().format(record)


class Log:
    """Log handling class. Root path can be overridden by env PROJECT_ROOT."""

    # Path to the current directory (this file: utils/log_util.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Project root: env PROJECT_ROOT wins; else two levels above this file (utils -> project_root)
    _default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.getenv('PROJECT_ROOT', _default_root)
    if not os.path.isabs(project_root):
        project_root = os.path.abspath(os.path.join(current_dir, project_root))

    # Path for general log files
    LOG_PATH = os.path.join(project_root, "log")
    # Path for user-specific log files
    USER_LOG_PATH = os.path.join(project_root, "log", "sift")

    # RotatingFileHandler: max single file 10MB, keep 10 backups
    LOG_MAX_BYTES = 10 * 1024 * 1024
    LOG_BACKUP_COUNT = 10

    @classmethod
    def init(cls, user=None):
        """Initialization process"""

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

    @classmethod
    def get_logger(cls, user: str = "unknown_user") -> Logger:
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


currentLog = Log()


class LoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['user'], msg), kwargs
