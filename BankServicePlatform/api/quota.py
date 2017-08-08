# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota,quota_record,quota_used_record
from ..tools import helper
from .import route

bp=Blueprint('quota',__name__,url_prefix='/quota')


@route(bp,'/<quota_id>')
def show(quota_id):
    """
        查找单个
    """
    return helper.show_result_content(quota.get_or_404(quota_id))

"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return helper.show_result_content(quota.create(**request.json))

@route(bp,'/<quota_id>',methods=['PUT'])
def update(quota_id):
    return helper.show_result_content(quota.update(quota.get_or_404(quota_id),**request.json))

@route(bp,'/<quota_id>',methods=['DELETE'])
def delete(quota_id):
    quota.delete(quota.get_or_404(quota_id))
    return None,204

"""==============================================额度调整记录====================================================="""
@route(bp,'/<quota_id>/records')
def records(quota_id):
    quota.get_or_404(quota_id).quota_recordes

@route(bp,'/<quota_id>/records/<quota_record_id>',methods=['PUT'])
def add_record(quota_id,quota_record_id):
    quota.add_quota_record(quota.get_or_404(quota_id),quota_record.get_or_404(quota_record_id))
    return None,204

"""==============================================额度使用记录====================================================="""
@route(bp,'/<quota_id>/used_record')
def used_record(quota_id):
    quota.get_or_404(quota_id).quota_used_recordes

@route(bp,'/<quota_id>/used_record/<quota_used_record_id>',methods=['PUT'])
def add_used_record(quota_id,quota_used_record_id):
    quota.add_quota_used_record(quota.get_or_404(quota_id),quota_used_record.get_or_404(quota_used_record_id))
    return None,204
