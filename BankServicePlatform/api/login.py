# -*- coding: utf-8 -*-
# __author__ = 'Johnny'
#
from flask import Blueprint,request,g

from . import route_nl

from ..core import  redis

from ..models import Customer

bp = Blueprint('login', __name__,url_prefix='/login')

@route_nl(bp,'/',methods=['POST'])
def login():
    phone=dict(**request.json)['phone']
    password=dict(**request.json)['password']
    openid=dict(**request.json)['openid']

    customer=Customer.query.filter_by(phone=phone).first()
    result=customer.verify_password(password)

    if result:
        g.customer=customer
        token=g.customer.generate_auth_token()
        redis.set(openid,token)
        return 'Success',200
        # return token.decode('ascii'),200
    else:
        return "Failed",400


@route_nl(bp,'/get_token',methods=['GET'])
def get_token():
    openid=dict(**request.json)['openid']
    return redis.get(openid)