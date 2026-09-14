from functools import wraps


def api(tags):
    """TODO: @api"""

    def wrapper(fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            # Decoration code goes here...
            return fn(*args, **kwargs)

        return decorated_fn

    return wrapper


def api_operation(value):
    """TODO: @api_operation"""

    def wrapper(fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            # Decoration code goes here...
            return fn(*args, **kwargs)

        return decorated_fn

    return wrapper
