# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request,jsonify
from ..services import quota,quota_record,quota_used_record
from ..tools import helper
import urllib
import urllib2
from .import route,route_nl
import json,yaml
from ..config import PAD_SERVER_URL,logger
import datetime

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
    #todo:增加额度验证，写操作改为事务
    try:
        request_json=dict(**request.json)

        quota_id=request_json['quota_id']
        _quota=quota.get(quota_id)

        if not _quota.isNone():
            original_quota=_quota.amount
            updated_quota=request_json['updated_quota']

            data={
                "quota_id":quota_id,
                "original_quota":original_quota,
                "updated_quota":updated_quota
            }
            quota_record.create(**data)
            _quota=quota.update(_quota,amount=updated_quota)
    except:
        logger.exception("error")
        return helper.show_result_fail("额度更新失败")

    return helper.show_result_data_success("额度更新成功",_quota)

@route(bp,'/<quota_id>',methods=['DELETE'])
def delete(quota_id):
    quota.delete(quota.get_or_404(quota_id))
    return None,204


#==================================PAD交互=====================================
@route_nl(bp,'/pad_increase_amount/<quota_id>')
def pad_increase_amount(quota_id):
    _quota=quota.get(quota_id)
    if not _quota.isNone():
        quota.update(_quota,status=0)
        try:
        # _quota_bill=quota.get_or_404(quota_id).quota_used_recordes.first().quota_billes
            _cutomer=_quota.customer
            data={
                "id":_quota.id,
                "customerName":_cutomer.real_name,
                "sfzh":str(_cutomer.identification_number),
                "phoneNo":_cutomer.phone,
                "cardNum":_cutomer.bank_card_number,
                "applyAmt":_quota.amount,
                "loanTerm":0,
                "applyTime":datetime.datetime.now()
            }
            data=urllib.urlencode(data)

            req=urllib2.Request("http://"+PAD_SERVER_URL+":8080/PCCredit/ipad/ks/getQuotaApply.json",data=data)
            response=urllib2.urlopen(req,timeout=60)

            response_json=yaml.safe_load(json.loads(response.read(),encoding='utf8'))
            result=response_json.get('result',None)
            status=result.get('status',None)
        except:
            logger.exception("error")
            return helper.show_result_fail("提额失败")

        if status=='success':
            return helper.show_result_success("提额成功")

        return helper.show_result_fail("提额失败")
    else:
        return helper.show_result_fail("没有记录")


@route_nl(bp,'/pad_update_amount',methods=['POST'])
def pad_update_amount():
    #todo:增加额度验证，写操作改为事务
    try:
        request_json=dict(**request.json)

        quota_id=request_json['quota_id']
        _quota=quota.get_or_404(quota_id)
        quota.update(_quota,status=1)

        original_quota=_quota.amount

        updated_quota=request_json['updated_quota']

        if isinstance(updated_quota,unicode):
            updated_quota=updated_quota.encode('utf8')

        updated_quota=str(updated_quota)

        data={
            "quota_id":quota_id,
            "original_quota":original_quota,
            "updated_quota":updated_quota
        }
        quota_record.create(**data)
        available_amount=float(_quota.available_amount)
        available_amount=float(float(updated_quota)-float(original_quota)+available_amount)

        if available_amount>0:
            available_amount=available_amount
        else:
            available_amount=0

        quota_data={
            "amount":updated_quota,
            "available_amount":available_amount
        }
        _quota=quota.update(_quota,**quota_data)
    except:
        logger.exception("error")
        return helper.show_result_fail("额度更新失败")

    return helper.show_result_data_success("额度更新成功",_quota)