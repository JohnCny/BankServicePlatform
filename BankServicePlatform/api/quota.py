# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request,jsonify
from ..services import quota,quota_record,quota_used_record
from ..tools.json_encoding import DateEncoder
import urllib
import urllib2
from .import route,route_nl
import json

bp=Blueprint('quota',__name__,url_prefix='/quota')


@route(bp,'/<quota_id>')
def show(quota_id):
    """
        查找单个
    """
    return quota.get_or_404(quota_id)

@route(bp,'/<quota_id>/quota_record')
def show_quota_record(quota_id):
    """
    查找每一笔额度变化记录
    :param quota_id:
    :return:
    """
    return quota.get_or_404(quota_id).quota_recordes.all()

@route(bp,'/<quota_id>/quota_used_record')
def show_quota_used_record(quota_id):
    """
    查找额度使用记录
    :param quota_id:
    :return:
    """
    return quota.get_or_404(quota_id).quota_used_recordes.all()


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return quota.create(**request.json)

@route(bp,'/<quota_id>',methods=['PUT'])
def update(quota_id):
    return quota.update(quota.get_or_404(quota_id),**request.json)

@route(bp,'/update_amount',methods=['POST'])
def update_amount():
    #todo:增加额度验证
    request_json=dict(**request.json)

    quota_id=request_json['quota_id']
    _quota=quota.get_or_404(quota_id)

    original_quota=_quota.amount
    updated_quota=request_json['updated_quota']

    data={
        "quota_id":quota_id,
        "original_quota":original_quota,
        "updated_quota":updated_quota
    }
    quota_record.create(**data)

    return quota.update(_quota,amount=updated_quota)

@route(bp,'/<quota_id>',methods=['DELETE'])
def delete(quota_id):
    quota.delete(quota.get_or_404(quota_id))
    return None,204


#==================================PAD交互=====================================
@route_nl(bp,'/pad_increase_amount/<quota_id>')
def pad_increase_amount(quota_id):
    _quota=quota.get_or_404(quota_id)
    _quota_bill=quota.get_or_404(quota_id).quota_used_recordes.first().quota_billes
    _cutomer=_quota.customer
    data={
        "id":_quota.id,
        "customerName":_cutomer.real_name,
        "cardId ":_cutomer.identification_number,
        "phoneNo":_cutomer.phone,
        "cardNum":_cutomer.bank_card_number,
        "applyAmt":_quota.amount,
        "loanTerm":_quota_bill.period,
        "applyTime":_quota_bill.create_date
    }
    data=urllib.urlencode(data)
    req=urllib2.Request("http://192.168.3.38:8080/pccredit_remote/ipad/ks/getQuotaApply.json",data=data)
    response=urllib2.urlopen(req,timeout=60)
    # response_json=json.loads(response.read(),encoding='utf8')
    # status=response_json.get('status',None)
    code=response.getcode()
    if code=='200':
        response_json=dict(response.read())
        status=response_json.get('status',None)
        if status:
            if status=='Success':
                return 'Success',200
    return 'Failed',200


@route_nl(bp,'/pad_update_amount',methods=['POST'])
def pad_update_amount():
    #todo:增加额度验证
    request_json=dict(**request.json)

    quota_id=request_json['quota_id']
    _quota=quota.get_or_404(quota_id)

    original_quota=_quota.amount
    updated_quota=request_json['updated_quota']

    data={
        "quota_id":quota_id,
        "original_quota":original_quota,
        "updated_quota":updated_quota
    }
    quota_record.create(**data)

    return quota.update(_quota,amount=updated_quota)