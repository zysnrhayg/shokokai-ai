#py_util_exception.vm
# Custom exception classes for API and DB layer; catch these before Exception in controllers/utils.

from functools import wraps
import traceback
from flask import g, request, session 
import utils.config


class ValidationError(Exception):
    """Raised when request validation fails (missing/invalid params)."""
    def __init__(self, message=None, code=None):
        self.message = message or "validation_failed"
        self.code = code or "validation_failed"
        super().__init__(self.message)


class NotFoundError(Exception):
    """Raised when a requested resource is not found."""
    def __init__(self, message=None, code=None):
        self.message = message or "not_found"
        self.code = code or "not_found"
        super().__init__(self.message)


class DBError(Exception):
    """Raised when a database operation fails (connection, constraint, etc.)."""
    def __init__(self, message=None, code=None):
        self.message = message or "db_error"
        self.code = code or "db_error"
        super().__init__(self.message)


# Decorator to catch exceptions and log them
def catch_excetion(msg: str = None):

    # msg is for custom function messages
    def except_execute(func):
        msg2 = msg

        @wraps(func)
        def execept_print(*args, **kwargs):
            try:
                # Custom function func
                return func(*args, **kwargs)
            except Exception as e:
                sign = "=" * 60 + "\n"
                if msg2 is None:
                    msg_ = e.__class__.__name__
                else:
                    msg_ = msg2
                # Log the exception information
                utils.config.global_log.error(f">>>{func.__name__}(): {msg_}:\t{e}")
                utils.config.global_log.error(f"{sign}{traceback.print_exc()}{sign}")

        return execept_print

    return except_execute


def log_exception(e: Exception):
    """Function to log exceptions"""
    msg_ = e.__class__.__name__
    utils.config.global_log.error(f">>> A global error has been detected: {msg_}: {e}")
    utils.config.global_log.error(f">>> URL: {request.url}")
    utils.config.global_log.error(traceback.format_exc())
