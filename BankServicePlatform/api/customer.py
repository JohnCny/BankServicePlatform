# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint
from ..services import customer
from ..tools import helper
from .import route

bp=Blueprint('customer',__name__,url_prefix='/customer')

@route(bp,'/')
def list():
    return helper.show_result_content(customer.all())
