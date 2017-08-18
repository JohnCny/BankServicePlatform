# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint, render_template


from . import route,route_nl




bp = Blueprint('frontend', __name__)

@route_nl(bp, '/')
def index():
    return render_template('mmdl.html')

@route_nl(bp, '/login')
def showlogin():
    return render_template('mmdl.html')

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
def wdyhk():
    return render_template('wdyhk.html')

#我的账户
@route(bp,'/wdzh')
def wdzh():
    return render_template('wdzh.html')

#我要贷款
@route(bp,'/wydk')
def wydk():
    return render_template('wydk.html')

#我要还款
@route(bp,'/wyhk')
def wyhk():
    return render_template('wyhk.html')

#提额申请
@route(bp,'/ysx')
def ysx():
    return render_template('ysx.html')

#我要贷款
@route(bp,'/dksqjl')
def dksqjl():
    return render_template('dksqjl.html')

#验证码登录
@route_nl(bp,'/yzmdl')
def yzmdl():
    return render_template('yzmdl.html')

#密码登录
@route(bp,'/mmdl')
def mmdl():
    return render_template('mmdl.html')

#注册
@route_nl(bp,'/zc')
def zc():
    return render_template('zc.html')

#找回密码
@route_nl(bp,'/zhmm')
def zhmm():
    return render_template('zhmm.html')
