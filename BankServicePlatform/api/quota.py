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
    request_json=dict(request.json)

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


