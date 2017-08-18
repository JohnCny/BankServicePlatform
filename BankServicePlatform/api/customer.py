# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import customer,quota
from passlib.apps import custom_app_context as pwd_context
from ..config import PAD_SERVER_URL,logger
from .import route,route_nl
from flask_login import login_user
from ..tools import helper,json_encoding
import urllib,urllib2,yaml,json
from ..models import QuotaRepayment, QuotaBill, QuotaUsedRecord, Quota, Customer
import datetime

bp=Blueprint('customer',__name__,url_prefix='/customer')


# @route(bp,'/')
# def list():
#     """
#         查询，返回全部
#     """
#     return customer.all()

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
    try:
        request_json=dict(**request.json)
        _cutomer=dict(request_json.get('customer'))

        _password=_cutomer['password']
        password=pwd_context.encrypt(_password)
        _cutomer['password']=password


        #验证身份证号码是否存在
        cus_phone_ls = customer.find(phone=_cutomer['phone']).all()
        if cus_phone_ls != None and len(cus_phone_ls)>0:
            return {"info":"电话号码已存在","result":"Failed"}

        cus_card_ls = customer.find(identification_number=_cutomer['identification_number']).all()
        if cus_card_ls != None and len(cus_card_ls)>0:
            return {"info":"证件号码已存在","result":"Failed"}

        request_json['customer']=_cutomer


        new_customer=customer.create(**request_json)
        login_user(new_customer)
        token=new_customer.generate_auth_token()
        set_init_quota(new_customer.id)
    except:
        logger.exception("error")
        return helper.show_result_fail("注册用户失败")

    return helper.show_result_data_success("注册用户成功",{"customer":new_customer,
            "token":token.decode('ascii')})

@route(bp,'/<customer_id>',methods=['PUT'])
def update(customer_id):
    return customer.update(customer.get_or_404(customer_id),**request.json)

@route(bp,'/<customer_id>',methods=['DELETE'])
def delete(customer_id):
    customer.delete(customer.get_or_404(customer_id))
    return None,204

@route(bp,'/<customer_id>/add_bank_card',methods=['POST'])
def add_bank_card(customer_id):
    try:
        _customer=customer.update(customer.get_or_404(customer_id),**request.json)
        update_quota(_customer.id,_customer.identification_number,_customer.real_name,_customer.phone,_customer.bank_card_number)
    except:
        logger.exception("error")
        return helper.show_result_fail("新增银行卡失败")

    return helper.show_result_data_success("新增银行卡成功",customer.get_or_404(customer_id))


def set_init_quota(customer_id):
    quota_data={
            "customer_id":customer_id,
            "amount":0,
            "available_amount":0
    }
    quota.create(**quota_data)


def update_quota(customer_id,identification_number,real_name,phone,bank_card_number):
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

    update_quota=result.get('quota',None).encode('utf8')

    available_amount=int(_quota.available_amount)
    available_amount=int(int(update_quota)-int(_quota.amount)+available_amount)

    if available_amount>0:
        available_amount=available_amount
    else:
        available_amount=0

    quota_data={
        "amount":update_quota,
        "available_amount":available_amount
    }

    quota.update(_quota,**quota_data)#todo:重复

    return True

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

@route(bp,'/repayments/<customer_id>')
def show_customer_repayments(customer_id):
    """
        查找用户show_customer_repayments
    """
    GMT_FORMAT = '%Y-%b-%d %H:%M:%S'
    _res = QuotaRepayment.query.join(QuotaBill).join(QuotaUsedRecord).join(Quota).join(Customer).filter \
            (Customer.id == customer_id,
             QuotaRepayment.is_repaid == 0).order_by(QuotaRepayment.period).all()
    for obj in _res:
        obj.final_repayment_date = str(obj.final_repayment_date)[0:10]
        
    return _res

@route(bp,'/quota_used_recordes/<customer_id>')
def show_customer_quota_used_recordes(customer_id):
    """
        查找全部quota_used_recordes
    """
    return customer.get_or_404(customer_id).quotaes.quota_used_recordes.all()