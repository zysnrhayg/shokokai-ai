#mysql_utils.py
#py_mysql_utils.vm make python connect database
# 数据库配置来源：config 从 settings.toml（由 PROJECT_ROOT 定位）直接读取，run.py 启动时设置 PROJECT_ROOT
# Slow-query monitoring: set SLOW_QUERY_THRESHOLD_SECONDS (default 1.0); query_sql_with_timing logs when exceeded.
# Indexing: recommend indexes on frequently filtered columns and foreign keys used in JOINs.
import inspect
import os
import time
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Text, text, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session as OrmSession, sessionmaker, scoped_session
from flask import session 
import utils.config
from utils.exception_util import DBError
from config import get_database_uri

# Same config source as run.py: config.get_database_uri() reads from settings.toml (tomllib) + env
DATABASE_URI = get_database_uri() or os.getenv("DATABASE_URI")
if not DATABASE_URI:
    raise RuntimeError("DATABASE_URI or config DB_* must be set")
# SQL_ECHO 优先从 config 读（含 settings.toml），否则用环境变量，这样 settings.toml 里 SQL_ECHO = true 才会生效
try:
    from config import SQL_ECHO as _sql_echo_cfg
    from config import SQL_LOG_MAX_LEN as _sql_log_max_len_cfg
    sql_echo = str(_sql_echo_cfg or "").lower() == "true"
except Exception:
    sql_echo = os.getenv("SQL_ECHO", "false").lower() == "true"
    _sql_log_max_len_cfg = None
pool_size = int(os.getenv("DB_POOL_SIZE", "8"))
pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "1800"))

SLOW_QUERY_THRESHOLD_SECONDS = float(os.getenv("SLOW_QUERY_THRESHOLD_SECONDS", "1.0"))
if _sql_log_max_len_cfg is not None:
    _SQL_LOG_MAX_LEN = int(_sql_log_max_len_cfg)
else:
    _SQL_LOG_MAX_LEN = int(os.getenv("SQL_LOG_MAX_LEN", "800"))


def _sql_caller_site() -> str:
    """First app/utils frame outside SQLAlchemy and mysqldb_utils."""
    project_root = (os.getenv("PROJECT_ROOT") or os.getcwd()).replace("\\", "/").rstrip("/")
    for fi in inspect.stack()[1:]:
        mod = fi.frame.f_globals.get("__name__", "") or ""
        if mod.startswith("sqlalchemy"):
            continue
        if mod == "utils.mysqldb_utils":
            continue
        path = (fi.filename or "").replace("\\", "/")
        if "/site-packages/" in path and project_root not in path:
            continue
        if project_root and path.startswith(project_root):
            path = path[len(project_root) + 1 :]
        return f"{path}:{fi.lineno} {fi.function}()"
    return "unknown"


def _compact_sql(statement: str) -> str:
    compact = " ".join((statement or "").split())
    if len(compact) > _SQL_LOG_MAX_LEN:
        return compact[:_SQL_LOG_MAX_LEN] + "..."
    return compact


def _register_sql_execution_logging(eng) -> None:
    """Log SQL with caller site when SQL_ECHO=true (replaces engine echo)."""

    @event.listens_for(eng, "before_cursor_execute")
    def _sql_log_before(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("_sql_log_stack", []).append(
            {
                "site": _sql_caller_site(),
                "statement": statement,
                "parameters": parameters,
                "started": time.perf_counter(),
            }
        )

    @event.listens_for(eng, "after_cursor_execute")
    def _sql_log_after(conn, cursor, statement, parameters, context, executemany):
        stack = conn.info.get("_sql_log_stack")
        if not stack:
            return
        ctx = stack.pop()
        elapsed_ms = (time.perf_counter() - ctx["started"]) * 1000
        utils.config.global_log.info(
            "SQL (%.1fms) @ %s | %s | params=%s",
            elapsed_ms,
            ctx["site"],
            _compact_sql(ctx["statement"]),
            ctx["parameters"],
        )

    @event.listens_for(OrmSession, "after_commit")
    def _sql_log_after_commit(sess):
        utils.config.global_log.info("SQL txn COMMIT @ %s", _sql_caller_site())

    @event.listens_for(OrmSession, "after_rollback")
    def _sql_log_after_rollback(sess):
        utils.config.global_log.info("SQL txn ROLLBACK @ %s", _sql_caller_site())

    from logger import silence_sqlalchemy_builtin_sql_logs

    silence_sqlalchemy_builtin_sql_logs()


engine = create_engine(
    DATABASE_URI,
    echo=False,
    pool_size=pool_size,
    pool_recycle=pool_recycle,
    pool_pre_ping=True,
)
if sql_echo:
    _register_sql_execution_logging(engine)
Session = scoped_session(sessionmaker(bind=engine))


def _materialize_rows_before_session_close(response):
    """Fetch all rows while the session/connection is still active. After Session.remove(),
    the Result is closed and cannot be read (and DML results do not return rows)."""
    if response is None:
        return []
    try:
        if hasattr(response, "returns_rows") and not response.returns_rows:
            return []
        return [dict(r) for r in response.mappings()]
    except Exception:
        return []


def query_sql_with_timing(sql, params=None):
    """Execute query and log if duration exceeds SLOW_QUERY_THRESHOLD_SECONDS. Use for slow-query monitoring."""
    session = Session()
    try:
        start = time.perf_counter()
        response = session.execute(text(sql), params or {})
        session.commit()
        elapsed = time.perf_counter() - start
        if elapsed >= SLOW_QUERY_THRESHOLD_SECONDS:
            utils.config.global_log.warning(
                "Slow query (%.3fs) @ %s | %s",
                elapsed,
                _sql_caller_site(),
                _compact_sql(sql),
            )
        return response
    except Exception as e:
        utils.config.global_log.error(e)
        session.rollback()
        raise
    finally:
        Session.remove()


# Unified transaction entry: use for write operations; insertSQL/updateSQL/delSQL already have try/except/finally internally.
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except DBError as e:
        utils.config.global_log.error("DBError: %s", e)
        session.rollback()
        raise
    except Exception as e:
        utils.config.global_log.error("DB operation failed: %s", e)
        session.rollback()
        raise DBError(str(e)) from e
    finally:
        Session.remove()

def result_to_list_of_dict(response):
    """Normalize query result to list of dict. Use for consistent Dao return shape."""
    if response is None:
        return []
    if isinstance(response, list):
        return response
    try:
        if hasattr(response, 'mappings'):
            return [dict(r) for r in response.mappings()]
        rows = response.fetchall()
        if not rows:
            return []
        keys = response.keys()
        return [dict(zip(keys, row)) for row in rows]
    except Exception as e:
        utils.config.global_log.error(e)
        return []

def check_connection():
    """Check DB connectivity. Returns (ok: bool, message: str). Used by /ready."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return (True, "")
    except DBError as e:
        utils.config.global_log.error("DBError: %s", e)
        return (False, str(e))
    except Exception as e:
        utils.config.global_log.error("DB check failed: %s", e)
        return (False, str(e))

def querySQL(sql, params=None):
	if not sql_echo:
		utils.config.global_log.debug(
			"SQL @ %s | %s | params=%s",
			_sql_caller_site(),
			_compact_sql(sql),
			params,
		)
	rows = None
	session = Session()
	try :
		response = session.execute(text(sql), params or {})
		rows = _materialize_rows_before_session_close(response)
		session.commit()
	except Exception as e:
		utils.config.global_log.error(e)
		session.rollback()
	finally :
		Session.remove()
	return rows

def querySQLNoParams(sql):
	if not sql_echo:
		utils.config.global_log.debug(
			"SQL @ %s | %s",
			_sql_caller_site(),
			_compact_sql(sql),
		)
	rows = None
	session = Session()
	try :
		response = session.execute(text(sql))
		rows = _materialize_rows_before_session_close(response)
		session.commit()
	except Exception as e:
		utils.config.global_log.error(e)
		session.rollback()
	finally :
		Session.remove()
	return rows

def delSQL(sql,params):
	if not sql_echo:
		utils.config.global_log.debug(
			"SQL @ %s | %s | params=%s",
			_sql_caller_site(),
			_compact_sql(sql),
			params,
		)
	response = None
	session = Session()
	try :
		response = session.execute(text(sql), params or {})
		session.commit()
	except Exception as e:
		utils.config.global_log.error(e)
		session.rollback()
	finally :
		Session.remove() 
		
	return response

def insertSQL(sql,params):
	if not sql_echo:
		utils.config.global_log.debug(
			"SQL @ %s | %s | params=%s",
			_sql_caller_site(),
			_compact_sql(sql),
			params,
		)
	response = None
	session = Session()
	try :
		response = session.execute(text(sql), params or {})
		session.commit()
	except Exception as e:
		utils.config.global_log.error(e)
		session.rollback()
	finally :
		Session.remove() 
		
	return response

def updateSQL(sql,params):
	if not sql_echo:
		utils.config.global_log.debug(
			"SQL @ %s | %s | params=%s",
			_sql_caller_site(),
			_compact_sql(sql),
			params,
		)
	response = None
	session = Session()
	try:
		response = session.execute(text(sql), params or {})
		session.commit()
	except Exception as e:
		utils.config.global_log.error(e)
		session.rollback()
		raise
	finally:
		Session.remove()
	return response
