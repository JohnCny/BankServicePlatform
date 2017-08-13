# -*- coding: utf-8 -*-
__author__ = 'Johnny'

"""
    BankServicePlatform.core
    ~~~~~~~~~~~~~
    core module
"""

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_redis import FlaskRedis

from flask import Flask
app = Flask(__name__)

# #: Flask-SQLAlchemy extension instance
db = SQLAlchemy()

#: Flask-Mail extension instance
mail = Mail()

#: Flask-Security extension instance
security = Security()

redis=FlaskRedis()


class BankServicePlatformError(Exception):
    """错误信息基类"""

    def __init__(self, msg):
        self.msg = msg


class BankServicePlatformFormError(Exception):
    """Form错误"""

    def __init__(self, errors=None):
        self.errors = errors


class Service(object):
    """
    sqlalchemy基础服务打包集合
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """
        实例检查
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """初始化模型
        :param kwargs: 参数集合
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """
        条件查询，返回全部
        :param **kwargs: 查询条件
        """
        return self.__model__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        """
        条件查询，返回第一条
        :param **kwargs: 查询条件
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        """
        页面回显用，无实例返回404
        :param id: id
        """
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        """
        新建实例
        :param **kwargs: 实例参数
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """
        新建实例，存入数据库
        :param **kwargs: 实例参数
        """
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        """
        更新
        :param model: 需要更新的model
        :param **kwargs: 更新参数
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()