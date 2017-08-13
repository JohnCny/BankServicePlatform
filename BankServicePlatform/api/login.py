# -*- coding: utf-8 -*-
# __author__ = 'Johnny'
#
from flask import Blueprint,request,g
import requests
import json

from . import route_nl

import urllib2 as urllib

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
    openid=get_wx_openid()
    return redis.get(openid)

def get_wx_openid():
    #获取用户code
    url="http://bsp.qkjr.com.cn/wdzh"
    url=url.decode('gbk','replace')
    redirect_uri=urllib.quote(url.encode('utf8','replace'))
    CODE_URL="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx8ca1ef28740b0106" \
             "&redirect_uri="+redirect_uri+"&response_type=code&scope=snsapi_base#wechat_redirect"
    response=requests.get(CODE_URL)
    print response.text
    code=json.loads(response.read()).get('code',None)
    print code
    #获取用户openid
    OPENID_URL="https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx8ca1ef28740b0106&secret=727125a17d9dd9d2508e7d3c46c85fbb" \
               "&code="+code+"&grant_type=authorization_code"
    response_oi=urllib.urlopen(OPENID_URL)
    openid=json.loads(response_oi.read()).get('openid',None)
    print openid
    return openid
