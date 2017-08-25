# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint, request
from ..services import quota_repayment, quota_bill, quota_used_record,quota
from ..tools import helper
from . import route, transaction
from ..models import QuotaRepayment, QuotaBill, QuotaUsedRecord, Quota, Customer
import datetime
from ..config import logger
import traceback


bp = Blueprint('quota_repayment', __name__, url_prefix='/quota/quota_repayment')


@route(bp, '/<quota_repayment_id>')
def show(quota_repayment_id):
    """
        查找单个
    """
    return quota_repayment.get_or_404(quota_repayment_id)


"""页面组成字典或者json"""


@route(bp, '/', methods=['POST'])
def new():
    # todo:增加事务,多期合并
    request_json_origin = dict(**request.json)
    request_json_origin = request_json_origin["repayments"]

    try:
        for _request in request_json_origin:
            request_json = dict(_request)
            
            quota_repayment_id = request_json['quota_repayment_id']
            repayment_amount = request_json['repayment_amount']
            _quota_repayment = quota_repayment.get_or_404(quota_repayment_id)

            if repayment_amount >= _quota_repayment.repayment_amount:
                _quota_bill = quota_bill.get(_quota_repayment.quota_bill_id)
                if not _quota_bill.isNone():
                    update_quota_bill(_quota_bill,_quota_repayment.principal)
                    repaid_data = {
                        "repaid": repayment_amount,
                        "is_repaid": 1,
                        "repayment_date": datetime.datetime.now()
                    }
                    quota_repayment.update(_quota_repayment,**repaid_data)
            else:
                repaid_data = {
                    "repaid": repayment_amount,
                    "repayment_date": datetime.datetime.now()
                }
                quota_repayment.update(**repaid_data)
    except:
        logger.exception("error")
        return helper.show_result_fail("还款失败")

    return helper.show_result_success("还款成功")


def update_quota_bill(_quota_bill,repaid_principal):
    period = _quota_bill.period_remain - 1
    _quota_used_record=quota_used_record.get(_quota_bill.quota_used_record_id)
    if not _quota_used_record.isNone():
        if period > 0:
            quota_bill.update(_quota_bill, period_remain=period)
        elif period == 0:
            quota_bill.update(_quota_bill, period_remain=period)
            update_quota_used_record(_quota_used_record)

    update_quota(_quota_used_record.quota_id,repaid_principal)


def update_quota_used_record(_quota_used_record):
    #为了配合前端参数预编译
    update_data={
        "quota_used_record":{"status":1}
    }
    _quota_used_record=quota_used_record.update(_quota_used_record, **update_data)

def update_quota(quota_id,repaid_principal):
    _quota=quota.get(quota_id)
    if not _quota.isNone():
        updated_amount=float(_quota.available_amount)+float(repaid_principal)
        return quota.update(_quota,available_amount=updated_amount)
    return _quota


@route(bp, '/<customer_id>/get_expected_repayment_7d', methods=['GET'])
def get_expected_repayment_7d(customer_id):
    try:
        date_7d=datetime.date.today()+datetime.timedelta(days=7)

        data = QuotaRepayment.query.join(QuotaBill).join(QuotaUsedRecord).join(Quota).join(Customer).filter \
            (Customer.id == customer_id,
             QuotaRepayment.final_repayment_date <= date_7d,
             QuotaRepayment.is_repaid == 0)

        query_data = data.all()
        total = 0
        for repayments in query_data:
            total += repayments.repayment_amount


    except:
        logger.exception("error")
        return helper.show_data_fail(None)

    return helper.show_data_success(total)
