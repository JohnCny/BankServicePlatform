# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_record
from ..tools import helper
from ..config import logger
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
    try:
        _quota_record=quota_record.create(**request.json)
    except:
        logger.exception("error")
        return helper.show_result_fail("贷款记录新增失败")

    return helper.show_result_data_success("贷款记录新增成功",_quota_record)


