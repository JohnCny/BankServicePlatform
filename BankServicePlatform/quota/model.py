# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import db
from ..tools.helper import JsonSerializer
from datetime import datetime

class QuotaJsonSerializer(JsonSerializer):
    __json_public__ = ["amount","available_amount"]

class Quota(QuotaJsonSerializer,db.Model):
    __tablename__="quota"

    id = db.Column(db.Integer(), primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'))
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'),default=1)#todo:今后需改为多产品
    amount=db.Column(db.Integer())#总额度
    available_amount=db.Column(db.Float(),default=0)#可用额度
    version=db.Column(db.Integer())#防并发，每次更新该值+1

    quota_recordes=db.relationship('QuotaRecord', backref='quota',lazy='dynamic')#额度记录
    quota_used_recordes=db.relationship('QuotaUsedRecord', backref='quota',lazy='select')#使用额度记录


class QuotaRecordJsonSerializer(JsonSerializer):
    __json_public__ = ["original_quota","updated_quota","create_date"]

class QuotaRecord(QuotaRecordJsonSerializer,db.Model):
    __tablename__="quota_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota_id=db.Column(db.Integer,db.ForeignKey('quota.id'))
    create_date=db.Column(db.DateTime(),default=datetime.now())#日期
    original_quota=db.Column(db.Integer())#原始额度
    updated_quota=db.Column(db.Integer())#变更后额度

class QuotaUsedRecordJsonSerializer(JsonSerializer):
    __json_public__ = ["used_quota","create_date","status"]

class QuotaUsedRecord(QuotaUsedRecordJsonSerializer,db.Model):
    __tablename__="quota_used_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota_id=db.Column(db.Integer,db.ForeignKey('quota.id'))
    used_quota=db.Column(db.Integer())#使用额度
    create_date=db.Column(db.DateTime(),default=datetime.now())#日期
    status=db.Column(db.Integer(),default=0)#当前状态

    quota_billes=db.relationship('QuotaBill', backref='quota_used_record',uselist=False)#额度账单

class QuotaBillJsonSerializer(JsonSerializer):
    __json_public__ = ["period_principal","period_interest","period_remain","create_date"]

class QuotaBill(QuotaBillJsonSerializer,db.Model):
    __tablename__="quota_bill"

    id = db.Column(db.Integer(), primary_key=True)
    quota_used_record_id=db.Column(db.Integer,db.ForeignKey('quota_used_record.id'))
    period_amount=db.Column(db.Float())#每期应还
    period_remain=db.Column(db.Integer())#剩余期数
    create_date=db.Column(db.DateTime(),default=datetime.now())#日期

    quota_repaymentes=db.relationship('QuotaRepayment', backref='quota_bill',lazy='dynamic')#账单还款记录

class QuotaRepaymentJsonSerializer(JsonSerializer):
    __json_public__ = ["repayment_amount","period","repayment_date"]

class QuotaRepayment(QuotaRepaymentJsonSerializer,db.Model):
    __tablename__="quota_repayment"

    id = db.Column(db.Integer(), primary_key=True)
    quota_bill_id=db.Column(db.Integer,db.ForeignKey('quota_bill.id'))
    repayment_amount=db.Column(db.Float())#还款金额
    period=db.Column(db.Integer())#期数
    repayment_date=db.Column(db.DateTime(),default=datetime.now())#日期


