# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request

from . import route

from ..services import customer

bp = Blueprint('login', __name__,url_prefix='/login')

@route(bp,'/',methods=['POST'])
def login():
    result=customer.first(**request.json)
    if result:
        return "Success",200
    else:
        return "Failed",400