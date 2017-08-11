# -*- coding: utf-8 -*-
__author__ = 'Johnny'

import os

from celery import Celery
from flask import Flask

from flask_httpauth import HTTPBasicAuth

from .core import db
from .tools.helper import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware
from .models import Customer
from flask import g



auth=HTTPBasicAuth()

def create_app(package_name, package_path,settings_overrde=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the bankserviceplatform platform.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults
                                        to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('BankServicePlatform.config')
    # app.config.from_object(settings_override)

    db.init_app(app)

    # login_manager.init_app(app)

    # mail.init_app(app)
    # security.init_app(app, SQLAlchemyUserDatastore(db, Customer,Role),
    #                   register_blueprint=register_security_blueprint)

    register_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app


def create_celery_app(app=None):
    app = app or create_app('bankserviceplatform', os.path.dirname(__file__))
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# @login_manager.unauthorized_handler
# def unauthorized():
#     flash('需要登录','error')
#     return render_template("mmdl.html"),500
#
# @login_manager.user_loader
# def load_user(id):
#     return Customer.query.get(int(id))

@auth.verify_password
def verify_password(phone_or_token,password):
    if not password:
        return False
    customer=Customer.verify_auth_token(phone_or_token)
    if not customer:
        cp={
            "phone":phone_or_token,
            "password":password
        }
        customer=Customer.query.filter_by(phone=phone_or_token).first()
        if not customer or not customer.verify_password(password):
            return False

    g.customer=customer
    return True

@auth.error_handler
def unauthorized():
    return 'UnAuthorized',500