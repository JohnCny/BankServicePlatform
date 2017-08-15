# -*- coding: utf-8 -*-
# __author__ = 'Johnny'
#
from flask import Blueprint,request,redirect,g,jsonify,flash

import json

from . import route_nl,route

import urllib2 as urllib

from ..core import  redis
from ..factory import verify_password
from ..models import Customer
from flask_login import login_user,logout_user
from ..tools import helper

bp = Blueprint('login', __name__,url_prefix='/login')



@route_nl(bp,'/',methods=['POST'])
def login():
    """
    传入手机号码和获得的openid，将opeid和token的匹配写入redis
    :return:
    """

    phone=dict(**request.json)['phone']
    password=dict(**request.json)['password']
    openid=dict(**request.json)['openid']

    # customer=Customer.query.filter_by(phone=phone).first()
    #
    # result=customer.verify_password(password)
        # if result:
    #     customer=Customer.query.filter_by(phone=phone).first()
    #     token=g.customer.generate_auth_token()
    #     #redis.set(openid,token,ex=3600*24*7)
    #     return 'Success',200
    # else:
    #     return "Failed",400\
    try:
        result=verify_password(phone,password)
    except:
        return helper.show_result_fail("用户名或者密码错误")
    if result:
        g.customer=Customer.query.filter_by(phone=phone).first()
        login_user(g.customer)
        token=g.customer.generate_auth_token()
        redis.set(openid,token)
        return {"customer":g.customer,"token":token}
    else:
        g.customer=None
        return {"info":"用户名或者密码错误","result":"Failed"}


@route_nl(bp,'/get_token_by_openid')
def get_token_by_openid():
    openid=dict(**request.json)['openid']
    token=redis.get(openid)
    if token:
        return token,200
    else:
        return "Need Logged In",500

@bp.route('/get_token')
def get_token():
    # access_token=redis.get("access_token",None)
    # if access_token:
    #     openid=dict(**request.json)['openid']
    # else:
    #     response_at=urllib.urlopen('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx8ca1ef28740b0106&secret=727125a17d9dd9d2508e7d3c46c85fbb')
    #     access_token_get=json.loads(response_at.read()).get('access_token',None)
    #     if access_token_get:
    #         expires_in=json.loads(response_at.read()).get('expires_in',None)
    #         redis.set("access_token",access_token_get,ex=expires_in)
    #
    #         openid=dict(**request.json)['openid']
    #     else:
    #         return "GET WX_ACCESS_TOKEN FAILED",500

    #获取用户code
    redirect_uri="http%3a%2f%2fbsp.qkjr.com.cn%2fapi%2flogin%2fget_openid"
    CODE_URL="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx8ca1ef28740b0106" \
             "&redirect_uri="+redirect_uri+"&response_type=code&scope=snsapi_base#wechat_redirect"
    return redirect(CODE_URL)



@bp.route('/get_openid')
def get_openid():
    #获得openid
    code=request.args['code']
    OPENID_URL="https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx8ca1ef28740b0106&secret=727125a17d9dd9d2508e7d3c46c85fbb" \
               "&code="+code+"&grant_type=authorization_code"
    response_oi=urllib.urlopen(OPENID_URL)
    openid=json.loads(response_oi.read()).get('openid',None)

    if openid:
        redis.set(openid,None)
        return jsonify(openid)


@bp.route('/log_out')
def log_out():
    logout_user()
    return redirect('/login')