# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from BankServicePlatform import db
from ..tools.helper import JsonSerializer
import datetime

class CustomerJsonSerializer(JsonSerializer):
    __json_public__ = ["real_name","identification_number","phone"]

class Customer(CustomerJsonSerializer,db.Model):
    __tablename__="customer"

    id = db.Column(db.Integer(), primary_key=True)

    password=db.Column(db.String(32))
    real_name=db.Column(db.String(8))#姓名
    identification_number=db.Column(db.String(20))#身份证
    phone=db.Column(db.String(20))#手机号码
    channel=db.Column(db.Integer())#渠道
    create_date=db.Column(db.DateTime(),default=datetime.datetime.now())#创建时间

    quotaes=db.relationship('Quota', backref='customer',uselist=False)#额度关联

