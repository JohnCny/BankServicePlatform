# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_repayment,quota_bill,quota_used_record
from ..tools import helper
from .import route

bp=Blueprint('quota_repayment',__name__,url_prefix='/quota/quota_repayment')

@route(bp,'/<quota_repayment_id>')
def show(quota_repayment_id):
    """
        查找单个
    """
    return quota_repayment.get_or_404(quota_repayment_id)


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    #todo:增加事务,多期合并

    request_json=dict(**request.json)
    quota_bill_id=request_json['quota_bill_id']
    repayment_amount=request_json['repayment_amount']

    _quota_bill=quota_bill.get_or_404(quota_bill_id)
    if repayment_amount>=_quota_bill.period_amount:
        update_quota_bill(_quota_bill)

    return quota_repayment.create(**request.json)

def update_quota_bill(_quota_bill):
    period=_quota_bill.period_remain-1
    if period>0:
        quota_bill.update(_quota_bill,period_remain=period)
        return True
    elif period==0:
        quota_bill.update(_quota_bill,period_remain=period)
        update_quota_used_record(_quota_bill.quota_used_record_id)
        return True

    return False

def update_quota_used_record(quota_used_record_id):
    return quota_used_record.update(quota_used_record.get_or_404(quota_used_record_id),status=1)


@route(bp,'/<quota_repayment_id>',methods=['PUT'])
def update(quota_repayment_id):
    return quota_repayment.update(quota_repayment.get_or_404(quota_repayment_id),**request.json)

@route(bp,'/<quota_repayment_id>',methods=['DELETE'])
def delete(quota_repayment_id):
    quota_repayment.delete(quota_repayment.get_or_404(quota_repayment_id))
    return None,204