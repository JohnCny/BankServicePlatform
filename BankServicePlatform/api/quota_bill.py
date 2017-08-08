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
    return helper.show_result_content(quota_bill.get_or_404(quota_bill_id))


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return helper.show_result_content(quota_bill.create(**request.json))

@route(bp,'/<quota_bill_id>',methods=['PUT'])
def update(quota_bill_id):
    return helper.show_result_content(quota_bill.update(quota_bill.get_or_404(quota_bill_id),**request.json))

@route(bp,'/<quota_bill_id>',methods=['DELETE'])
def delete(quota_bill_id):
    quota_bill.delete(quota_bill.get_or_404(quota_bill_id))
    return None,204

"""==============================================还款记录====================================================="""
@route(bp,'/<quota_bill_id>/repayments')
def repayments(quota_bill_id):
    quota_bill.get_or_404(quota_bill_id).quota_repaymentes

@route(bp,'/<quota_bill_id>/repayments/<quota_repayments_id>',methods=['PUT'])
def add_record(quota_used_record_id,quota_bill_id):
    quota_bill.add_quota_repayment(quota_bill.get_or_404(quota_used_record_id),quota_repayment.get_or_404(quota_bill_id))
    return None,204