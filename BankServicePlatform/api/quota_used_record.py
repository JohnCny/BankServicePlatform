# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_used_record,quota_bill,quota
from ..tools import helper
from .import route


bp=Blueprint('quota_used_record',__name__,url_prefix='/quota/quota_used_record')

@route(bp,'/<quota_used_record_id>')
def show(quota_used_record_id):
    """
        查找单个
    """
    return quota_used_record.get_or_404(quota_used_record_id)


@route(bp,'/<quota_used_record_id>/quota_bill')
def show_quota_bill(quota_used_record_id):
    """
    查找所有账单
    :param quota_used_record_id:
    :return:
    """
    return quota_used_record.get_or_404(quota_used_record_id).quota_billes

"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():

    #todo:需要增加事务

    quota_used_record_json=dict(dict(**request.json)['quota_used_record'])
    request_json=dict(**request.json)
    #获得可用余额和要使用的金额
    quota_id=quota_used_record_json['quota_id']
    used_quota=float(quota_used_record_json['used_quota'])
    avaliable_amount=float(quota.get_or_404(quota_id).available_amount)
    avaliable_remain=avaliable_amount-used_quota
    #获得利率和期限
    rate=0.18#todo:从产品获取利率
    period=float(request_json['period'])

    if avaliable_amount-used_quota>0:
        quota.update(quota.get_or_404(quota_id),available_amount=avaliable_remain)
        _quota_used_record=quota_used_record.create(**request.json)
        quota_used_record_id=_quota_used_record.id
        new_bill(used_quota,period,rate,quota_used_record_id)
        return helper.show_result_success("申请成功")
    else:
        return helper.show_result_fail("可用余额不足"),400


def new_bill(amount,period,rate,quota_used_record_id):
    period_amount=(amount*rate*(1+rate)**period)/((1+rate)**period-1)
    data={
        "quota_used_record_id":quota_used_record_id,
        "period_amount":period_amount,
        "period_remain":period
    }
    return quota_bill.create(**data)



