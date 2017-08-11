# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from functools import wraps

from flask import jsonify
from ..factory import auth
from ..core import BankServicePlatformError,BankServicePlatformFormError,login_manager
from ..tools.helper import JSONEncoder
from .. import factory




def create_app(settings_override=None):
    """Returns the bankserviceplatform API application instance"""

    app = factory.create_app(__name__, __path__, settings_override)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register custom error handlers
    app.errorhandler(BankServicePlatformError)(on_bankserviceplatform_error)
    app.errorhandler(BankServicePlatformFormError)(on_bankserviceplatform_form_error)
    app.errorhandler(404)(on_404)

    return app

def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @auth.login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), sc
        return f

    return decorator


def route_nl(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), sc
        return f

    return decorator


def on_bankserviceplatform_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_bankserviceplatform_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def on_404(e):
    return jsonify(dict(error='Not found')), 404





