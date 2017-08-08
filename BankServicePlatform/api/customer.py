# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint,request
from ..services import customer
from ..tools import helper
from .import route

bp=Blueprint('customer',__name__,url_prefix='/customer')

@route(bp,'/')
def list():
    """
        查询，返回全部
    """
    return customer.all()

@route(bp,'/<customer_id>')
def show(customer_id):
    """
        查找单个
    """
    return helper.show_result_content(customer.get_or_404(customer_id))


"""页面组成字典或者json"""
@route(bp,'/',methods=['POST'])
def new():
    return helper.show_result_content(customer.create(**request.json))

@route(bp,'/<customer_id>',methods=['PUT'])
def update(customer_id):
    return helper.show_result_content(customer.update(customer.get_or_404(customer_id),**request.json))

@route(bp,'/<customer_id>',methods=['DELETE'])
def delete(customer_id):
    customer.delete(customer.get_or_404(customer_id))
    return None,204

@route(bp,'/<customer_id>/quotas')
def quotas(customer_id):
    return customer.get_or_404(customer_id).quotaes

