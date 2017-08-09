# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint, render_template

from . import route



bp = Blueprint('/', __name__)


@route(bp, '/')
def index():
    return render_template('mmdl.html')

#用户
@route(bp,'/customer')
def customer():
    return render_template('customer.html')

#贷款详情
@route(bp,'/dkxq')
def dkxq():
    return render_template('dksqjl.html')

#还款确认
@route(bp,'/hkqr')
def hkqr():
    return render_template('hkqr.html')

#我的银行卡
@route(bp,'/wdyhk')
def hkqr():
    return render_template('wdyhk.html')

#我的账户
@route(bp,'/wdzh')
def hkqr():
    return render_template('wdzh.html')

#我要贷款
@route(bp,'/wydk')
def hkqr():
    return render_template('wydk.html')

#我要还款
@route(bp,'/wyhk')
def hkqr():
    return render_template('wyhk.html')

#提额申请
@route(bp,'/ysx')
def hkqr():
    return render_template('ysx.html')

#验证码登录
@route(bp,'/yzmdl')
def hkqr():
    return render_template('yzmdl.html')

#注册
@route(bp,'/zc')
def hkqr():
    return render_template('zc.html')

#找回密码
@route(bp,'/zhmm')
def hkqr():
    return render_template('zhmm.html')
