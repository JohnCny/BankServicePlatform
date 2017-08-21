# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_bill,quota_repayment,customer,quota,quota_used_record
from ..tools import helper
from .import route
from ..config import logger

bp=Blueprint('quota_bill',__name__,url_prefix='/quota/quota_bill')

@route(bp,'/<quota_bill_id>')
def show(quota_bill_id):
    """
        查找单个
    """
    return quota_bill.get_or_404(quota_bill_id)

@route(bp,'/')
def show_quota_billes():
    """
        查找全部
    """
    return quota_bill.all()


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
    try:
        _quota_bill=quota_bill.create(**request.json)
    except:
        logger.exception("error")
        helper.show_result_fail("账单新增失败")
    return helper.show_result_data_success("账单新增成功",_quota_bill)

