# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_record
from ..tools import helper
from .import route

bp=Blueprint('quota_record',__name__,url_prefix='/quota/quota_record')

@route(bp,'/<quota_record_id>')
def show(quota_record_id):
    """
        查找单个
    """
    return helper.show_result_content(quota_record.get_or_404(quota_record_id))


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return helper.show_result_content(quota_record.create(**request.json))

@route(bp,'/<quota_record_id>',methods=['PUT'])
def update(quota_record_id):
    return helper.show_result_content(quota_record.update(quota_record.get_or_404(quota_record_id),**request.json))

@route(bp,'/<quota_record_id>',methods=['DELETE'])
def delete(quota_record_id):
    quota_record.delete(quota_record.get_or_404(quota_record_id))
    return None,204

