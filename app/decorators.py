from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper


def admin_required(func):
    return permission_required(Permission.ADMINISTER)(func)
