# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_used_record,quota_bill
from ..tools import helper
from .import route

bp=Blueprint('quota_used_record',__name__,url_prefix='/quota/quota_used_record')

@route(bp,'/<quota_used_record_id>')
def show(quota_used_record_id):
    """
        查找单个
    """
    return helper.show_result_content(quota_used_record.get_or_404(quota_used_record_id))


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return helper.show_result_content(quota_used_record.create(**request.json))

@route(bp,'/<quota_used_record_id>',methods=['PUT'])
def update(quota_used_record_id):
    return helper.show_result_content(quota_used_record.update(quota_used_record.get_or_404(quota_used_record_id),**request.json))

@route(bp,'/<quota_used_record_id>',methods=['DELETE'])
def delete(quota_used_record_id):
    quota_used_record.delete(quota_used_record.get_or_404(quota_used_record_id))
    return None,204

"""==============================================已使用额度账单====================================================="""
@route(bp,'/<quota_used_record_id>/bills')
def bills(quota_used_record_id):
    quota_used_record.get_or_404(quota_used_record_id).quota_billes

@route(bp,'/<quota_used_record_id>/bills/<quota_bill_id>',methods=['PUT'])
def add_record(quota_used_record_id,quota_bill_id):
    quota_used_record.add_quota_bill(quota_used_record.get_or_404(quota_used_record_id),quota_bill.get_or_404(quota_bill_id))
    return None,204