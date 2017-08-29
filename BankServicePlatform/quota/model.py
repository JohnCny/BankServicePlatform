# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import db
from ..tools.helper import JsonSerializer
from datetime import datetime
from ..factories.models import BasicModel
from ..factories.gof import Singleton

class QuotaJsonSerializer(JsonSerializer):
    __json_public__ = ["id","amount","available_amount","status","is_bankcard_binded","is_none"]

class Quota(QuotaJsonSerializer,db.Model,BasicModel):
    __tablename__="quota"

    id = db.Column(db.Integer(), primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'))
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'),default=1)#todo:今后需改为多产品
    amount=db.Column(db.Integer())#总额度
    available_amount=db.Column(db.Float(),default=0)#可用额度
    version=db.Column(db.Integer())#防并发，每次更新该值+1
    status=db.Column(db.Integer(),default=1)#0不可提额，1可以提额
    is_bankcard_binded=db.Column(db.Integer(),default=0)#0未绑，1已绑

    quota_recordes=db.relationship('QuotaRecord', backref='quota',lazy='dynamic')#额度记录
    quota_used_recordes=db.relationship('QuotaUsedRecord', backref='quota',lazy='dynamic')#使用额度记录

class NoneQuota(Quota,Singleton):
    def isNone(self):
        return True


class QuotaRecordJsonSerializer(JsonSerializer):
    __json_public__ = ["id","original_quota","updated_quota","create_date","is_none"]

class QuotaRecord(QuotaRecordJsonSerializer,db.Model,BasicModel):
    __tablename__="quota_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota_id=db.Column(db.Integer,db.ForeignKey('quota.id'))
    create_date=db.Column(db.DateTime(),default=datetime.now())#日期
    original_quota=db.Column(db.Integer())#原始额度
    updated_quota=db.Column(db.Integer())#变更后额度

class NoneQuotaRecord(QuotaRecord,Singleton):
    def isNone(self):
        return True

class QuotaUsedRecordJsonSerializer(JsonSerializer):
    __json_public__ = ["id","used_quota","create_date","status","is_none"]

class QuotaUsedRecord(QuotaUsedRecordJsonSerializer,db.Model,BasicModel):
    __tablename__="quota_used_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota_id=db.Column(db.Integer,db.ForeignKey('quota.id'))
    used_quota=db.Column(db.Integer())#使用额度
    create_date=db.Column(db.DateTime(),default=datetime.now())#日期
    status=db.Column(db.Integer(),default=0)#当前状态

    quota_billes=db.relationship('QuotaBill', backref='quota_used_record',uselist=False)#额度账单

class NoneQuotaUsedRecord(QuotaUsedRecord,Singleton):
    def isNone(self):
        return True

class QuotaBillJsonSerializer(JsonSerializer):
    __json_public__ = ["id","period_amount","period","period_remain","create_date","is_none"]

class QuotaBill(QuotaBillJsonSerializer,db.Model,BasicModel):
    __tablename__="quota_bill"

    id = db.Column(db.Integer(), primary_key=True)
    quota_used_record_id=db.Column(db.Integer,db.ForeignKey('quota_used_record.id'))
    period_amount=db.Column(db.Float())#每期应还
    period=db.Column(db.Integer())#总期数
    period_remain=db.Column(db.Integer())#剩余期数
    create_date=db.Column(db.DateTime(),default=datetime.now())#日期

    quota_repaymentes=db.relationship('QuotaRepayment', backref='quota_bill',lazy='dynamic')#账单还款记录


class NoneQuotaBill(QuotaBill,Singleton):
    def isNone(self):
        return True

class QuotaRepaymentJsonSerializer(JsonSerializer):
    __json_public__ = ["id","repayment_amount","period","final_repayment_date","quota_bill_id","is_none"]

class QuotaRepayment(QuotaRepaymentJsonSerializer,db.Model,BasicModel):
    __tablename__="quota_repayment"

    id = db.Column(db.Integer(), primary_key=True)
    quota_bill_id=db.Column(db.Integer,db.ForeignKey('quota_bill.id'))
    repayment_amount=db.Column(db.Float())#还款金额
    period=db.Column(db.Integer())#期数
    principal=db.Column(db.Float())#应还本金
    interest=db.Column(db.Float())#应还利息
    repayment_date=db.Column(db.DateTime())#还款日期
    repaid=db.Column(db.Float())#已还金额 todo:今后需要区分已还本金还是利息
    is_repaid=db.Column(db.Integer())#是否已还清，0否，1是
    final_repayment_date=db.Column(db.DateTime())#最后还款日期

class NoneQuotaRepayment(QuotaRepayment,Singleton):
    def isNone(self):
        return True
