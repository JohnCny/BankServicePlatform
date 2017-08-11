# -*- coding: utf-8 -*-
# __author__ = 'Johnny'
#
from flask import Blueprint,request,g,jsonify

from . import route_nl

from ..services import customer
from ..models import Customer

bp = Blueprint('login', __name__,url_prefix='/login')

@route_nl(bp,'/',methods=['POST'])
def login():
    phone=dict(**request.json)['phone']
    password=dict(**request.json)['password']

    customer=Customer.query.filter_by(phone=phone).first()
    result=customer.verify_password(password)

    if result:
        g.customer=customer
        token=g.customer.generate_auth_token()
        return token.decode('ascii'),200
    else:
        return "Failed",400

