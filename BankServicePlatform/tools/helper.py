# -*- coding: utf-8 -*-
__author__ = 'Johnny'


import pkgutil
import importlib

from flask import Blueprint
from flask.json import JSONEncoder as BaseJSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta
import json




def register_blueprints(app, package_name, package_path):
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


class JSONEncoder(BaseJSONEncoder):

    def default(self, obj):
        if isinstance(obj, JsonSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JsonSerializer(object):

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv


# json转码
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data, ensure_ascii = False) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = str(data)
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

# 返回内容
def show_result_content(obj):
    return json.dumps(obj, cls=AlchemyEncoder,ensure_ascii = False) #json文本


# 返回成功提示
def show_result_success(info):
    return {"result":"Success","info":info}

# 返回失败提示
def show_result_fail(info):
    return {"result":"Failed","info":info}

# 返回成功提示以及数据
def show_result_data_success(info,data):
    return {"result":"Success","data":data,"info":info}

# 返回失败提示以及数据
def show_result_data_fail(info,data):
    return {"result":"Failed","data":data,"info":info}

# 返回成功数据
def show_data_success(data):
    return {"result":"Success","data":data}

# 返回失败数据
def show_data_fail(data):
    return {"result":"Failed","data":data}