# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_repayment
from ..tools import helper
from .import route

bp=Blueprint('quota_repayment',__name__,url_prefix='/quota/quota_repayment')

@route(bp,'/<quota_repayment_id>')
def show(quota_repayment_id):
    """
        查找单个
    """
    return helper.show_result_content(quota_repayment.get_or_404(quota_repayment_id))


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return helper.show_result_content(quota_repayment.create(**request.json))

@route(bp,'/<quota_repayment_id>',methods=['PUT'])
def update(quota_repayment_id):
    return helper.show_result_content(quota_repayment.update(quota_repayment.get_or_404(quota_repayment_id),**request.json))

@route(bp,'/<quota_repayment_id>',methods=['DELETE'])
def delete(quota_repayment_id):
    quota_repayment.delete(quota_repayment.get_or_404(quota_repayment_id))
    return None,204