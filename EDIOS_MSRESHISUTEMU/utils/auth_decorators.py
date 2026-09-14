from functools import wraps
from flask import abort, g
from flask_login import current_user
from flask_babel import gettext


# Retrieve user permissions
def roles_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not set(roles).issubset(set(current_user.roles)):
                abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def pre_authorize(auth_def):
    """Determine permissions

    @param auth_def - Permission expression, e.g.: hasAnyAuthority(["CYCLE10009|SELECT", "CYCLE10009|INSERT"])
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_fn(*args, **kwargs):
            # TODO: User.can(permissions)
            if not current_user.can(auth_def):
                abort(403)
            return fn(*args, **kwargs)

        return decorated_fn

    return wrapper


# Decorator used when login is required
def login_required(func):
    """Decorator function: Used when login is required."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "user") or not g.user:
            # Handle case where user is not logged in
            return (gettext("KS0048"), "warning")  # Display flash message
            # return redirect(url_for("auth.loginAuth"))  # Redirect to login page
        return func(*args, **kwargs)  # If user is logged in, execute the original function and return its result

    return decorated_function  # Return the decorated function


# Decorator used when logout is required
def logout_required(func):
    """Decorator function: Used when logout is required."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if hasattr(g, "user") and g.user:
            # Handle case where user is logged in
            return ("You are already authenticated.", "info")  # Display flash message
            # return redirect(url_for("index"))  # Redirect to index page
        return func(*args, **kwargs)  # If user is not logged in, execute the original function and return its result

    return decorated_function  # Return the decorated function


# Decorator used when account confirmation is required
def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if hasattr(g, "user") and g.user.isConfirmed is False:
            # Handle case where user has not confirmed their account
            return ("Please confirm your account!", "warning")  # Display flash message
            # return redirect(url_for("auth.emailAuthTransition"))  # Redirect to signup email sending page
        return func(*args, **kwargs)  # If user is confirmed, execute the original function and return its result

    return decorated_function  # Return the decorated function
