# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request,g
from ..services import customer
from ..tools import helper
from .import route,route_nl

bp=Blueprint('token',__name__,url_prefix='/token')

@route(bp,'/token')
def get_token():
    """
        根据openid获得token
    """
    result=customer.first(**request.json)
    if result:
        token=g.customer.generate_auth_token()
        return token.decode('ascii'),200
    else:
        return "Failed",400