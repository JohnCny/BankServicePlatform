# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import quota_used_record,quota_bill,quota,quota_repayment
from ..tools import helper
from ..config import logger
from .import route
import datetime


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
    try:
        quota_used_record_json=dict(dict(**request.json)['quota_used_record'])
        request_json=dict(**request.json)
        #获得可用余额和要使用的金额
        quota_id=quota_used_record_json['quota_id']
        used_quota=float(quota_used_record_json['used_quota'])
        avaliable_amount=float(quota.get_or_404(quota_id).available_amount)
        avaliable_remain=avaliable_amount-used_quota
        #获得利率和期限
        rate=0.015#todo:从产品获取利率
        period=int(request_json['period'])

        #判断可用余额
        if avaliable_amount-used_quota>0:
            quota.update(quota.get_or_404(quota_id),available_amount=avaliable_remain)
            _quota_used_record=quota_used_record.create(**request.json)
            quota_used_record_id=_quota_used_record.id

            #计算每月还本付息
            amount=(used_quota*rate*(1+rate)**period)/((1+rate)**period-1)
            #生成新的账单
            _quota_bill=new_bill(amount,period,quota_used_record_id)
            if _quota_bill:
                #生成新的还款记录
                _repayment=new_repayment(used_quota,amount,period,rate,_quota_bill.id)
                if _repayment:
                    return helper.show_result_success("申请用款成功")
                else:
                    return helper.show_result_fail("新增待还款记录失败")
            else:
                return helper.show_result_fail("新增账单失败")
        else:
            return helper.show_result_fail("可用余额不足")
    except:
        logger.exception("error")
        return helper.show_result_fail("申请用款失败")



def new_bill(amount,period,quota_used_record_id):

    data={
        "quota_used_record_id":quota_used_record_id,
        "period_amount":amount,
        "period_remain":period
    }
    return quota_bill.create(**data)

def new_repayment(used_quota,amount,period,rate,quota_bill_id):
    period_count=int(period)
    #计算每期还款明细
    while period_count:
        principal=used_quota*rate*(1+rate)**(period_count-1)/((1+rate)**period-1)
        interest=used_quota*rate*((1+rate)**(period)-(1+rate)**(period_count-1))/((1+rate)**period-1)
        frd=datetime.date.today()
        month=frd.month+period_count
        if month>12:
            frd=datetime.date(frd.year+1,month-12,frd.day)
        else:
            frd=datetime.date(frd.year,month,frd.day)
        repayment_data={
            "quota_bill_id":quota_bill_id,
            "repayment_amount":amount,
            "period":period_count,
            "repayment_date":None,
            "principal":principal,
            "interest":interest,
            "repaid":0,
            "is_repaid":0,
            "final_repayment_date":frd
        }
        try:
            quota_repayment.create(**repayment_data)
        except:
            logger.exception("error")
            return False
        period_count-=1

    return  True



