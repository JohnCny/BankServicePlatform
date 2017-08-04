__author__ = 'Johnny'
# -*- coding: utf-8 -*-
from ..core import db

class Customer(db.model):
    __tablename__="customer"

    id = db.Column(db.Integer(), primary_key=True)

    password=db.Column(db.String(32))
    real_name=db.Column(db.String(8))#姓名
    identification_number=db.Column(db.String(20))#身份证
    phone=db.Column(db.String(20))#手机号码
    channel=db.Column(db.Integer())#渠道
    create_date=db.Column(db.DateTime())#创建时间
