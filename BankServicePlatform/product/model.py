# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from BankServicePlatform import db

class Product(db.Model):
    __tablename__="product"

    id = db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(16))#产品名称
    interest_rate=db.Column(db.Float())#利率
    period=db.Column(db.Integer())#期数
    min_quota=db.Column(db.Integer())#最小额度
    max_quota=db.Column(db.Integer())#最大额度

    quotaes=db.relationship('Quota', backref='product',uselist=False)#额度关联