# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request,g
from ..services import customer,quota
from passlib.apps import custom_app_context as pwd_context
from ..config import PAD_SERVER_URL
from .import route,route_nl
from flask_login import login_user
import urllib,urllib2,yaml,json

bp=Blueprint('customer',__name__,url_prefix='/customer')


@route(bp,'/')
def list():
    """
        查询，返回全部
    """
    return customer.all()

@route(bp,'/<customer_id>/quota/')
def get_customer_quota(customer_id):
    """
    根据用户获得额度
    :return:
    """
    return customer.get_or_404(customer_id).quotaes


@route(bp,'/<customer_id>')
def show(customer_id):
    """
        查找单个
    """
    return customer.get_or_404(customer_id)

@route(bp,'/<customer_id>/quotas')
def quotas(customer_id):
    """
    查找每个用户的额度
    :param customer_id:
    :return:
    """
    return customer.get_or_404(customer_id).quotaes

"""页面组成字典或者json"""
@route_nl(bp,'/',methods=['POST'])
def new():
    request_json=dict(**request.json)
    _cutomer=dict(request_json.get('customer'))

    _password=_cutomer['password']
    password=pwd_context.encrypt(_password)
    _cutomer['password']=password

    request_json['customer']=_cutomer

    g.customer=customer.create(**request_json)
    login_user(g.customer)
    token=g.customer.generate_auth_token()
    return {"customer":g.customer,
            "token":token.decode('ascii')}

@route(bp,'/<customer_id>',methods=['PUT'])
def update(customer_id):
    return customer.update(customer.get_or_404(customer_id),**request.json)

@route(bp,'/<customer_id>',methods=['DELETE'])
def delete(customer_id):
    customer.delete(customer.get_or_404(customer_id))
    return None,204

@route(bp,'/<customer_id>/add_bank_card',methods=['POST'])
def add_bank_card(customer_id):
    _customer=customer.update(customer.get_or_404(customer_id),**request.json)
    set_init_quota(_customer.id,_customer.identification_number,_customer.real_name,_customer.phone,_customer.bank_card_number)
    return customer.get_or_404(customer_id)


def set_init_quota(customer_id,identification_number,real_name,phone,bank_card_number):
    data={

        "customerName":real_name,
        "sfzh":str(identification_number),
        "phoneNo":phone,
        "cardNum":bank_card_number
    }
    data=urllib.urlencode(data)
    req=urllib2.Request("http://"+PAD_SERVER_URL+":8080/PCCredit/ipad/ks/getCreditAmt.json",data=data)
    response=urllib2.urlopen(req,timeout=60)

    response_json=yaml.safe_load(json.loads(response.read(),encoding='utf8'))
    result=response_json.get('result',None)
    _quota=customer.get_or_404(customer_id).quotaes
    if not _quota:
        _quota=result.get('quota',None)
        _quota=int(_quota)
        quota_data={
            "customer_id":customer_id,
            "amount":_quota,
            "available_amount":_quota
        }
        return quota.create(**quota_data)#todo:重复

    return customer.get_or_404(customer_id).quotaes


@route(bp,'/quota_billes/<customer_id>')
def show_customer_billes(customer_id):
    """
        查找全部billes
    """
    return customer.get_or_404(customer_id).quotaes.quota_used_recordes.first().quota_billes

@route(bp,'/quota/<customer_id>')
def show_customer_quota(customer_id):
    """
        查找用户quota
    """
    return customer.get_or_404(customer_id).quotaes
	
@route(bp,'/quota_used_recordes/<customer_id>')
def show_customer_quota_used_recordes(customer_id):
    """
        查找全部quota_used_recordes
    """
    return customer.get_or_404(customer_id).quotaes.quota_used_recordes.all()