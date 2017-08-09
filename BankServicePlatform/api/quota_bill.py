# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_bill,quota_repayment
from ..tools import helper
from .import route

bp=Blueprint('quota_bill',__name__,url_prefix='/quota/quota_bill')

@route(bp,'/<quota_bill_id>')
def show(quota_bill_id):
    """
        查找单个
    """
    return quota_bill.get_or_404(quota_bill_id)

@route(bp,'/<quota_bill_id>/repayment')
def show_repayment(quota_bill_id):
    """
    查找每笔账单还款情况
    :param quota_bill_id:
    :return:
    """
    return quota_bill.get_or_404(quota_bill_id).quota_repaymentes.all()


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return quota_bill.create(**request.json)

@route(bp,'/<quota_bill_id>',methods=['PUT'])
def update(quota_bill_id):
    return quota_bill.update(quota_bill.get_or_404(quota_bill_id),**request.json)

@route(bp,'/<quota_bill_id>',methods=['DELETE'])
def delete(quota_bill_id):
    quota_bill.delete(quota_bill.get_or_404(quota_bill_id))
    return None,204

