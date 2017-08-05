# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from BankServicePlatform import db


class Quota(db.model):
    __tablename__="quota"

    id = db.Column(db.Integer(), primary_key=True)
    customer=db.Column(db.Integer,db.ForeignKey('customer.id'))
    product=db.Column(db.Integer,db.ForeignKey('product.id'))
    amount=db.Column(db.Integer())#总额度
    available_amount=db.Column(db.Float())#可用额度
    version=db.Column(db.Integer())#防并发，每次更新该值+1

    quota_recordes=db.relationship('QuotaRecord', backref='quota',lazy='dynamic')#额度记录
    quota_user_recordes=db.relationship('QuotaUseRecord', backref='quota',lazy='dynamic')#使用额度记录

class QuotaRecord(db.model):
    __tablename__="quota_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota=db.Column(db.Integer,db.ForeignKey('quota.id'))
    create_date=db.Column(db.Datetime())#日期
    original_quota=db.Column(db.Integer())#原始额度
    updated_quota=db.Column(db.Integer())#变更后额度

class QuotaUseRecord(db.model):
    __tablename__="quota_use_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota=db.Column(db.Integer,db.ForeignKey('quota.id'))
    useed_quota=db.Column(db.Integer())#使用额度
    create_date=db.Column(db.Datetime())#日期
    status=db.Column(db.Integer())#当前状态

    quota_billes=db.relationship('QuotaBill', backref='quota_used',lazy='dynamic',uselist=False)#额度账单

class QuotaBill(db.model):
    __tablename__="quota_bill"

    id = db.Column(db.Integer(), primary_key=True)
    quota_used=db.Column(db.Integer,db.ForeignKey('quota_used.id'))
    period_amount=db.Column(db.Float())#每期还款金额
    period_remain=db.Column(db.Integer())#剩余期数
    create_date=db.Column(db.Datetime())#日期

    quota_repaymentes=db.relationship('QuotaRepayment', backref='quota_bill',lazy='dynamic')#账单还款记录

class QuotaRepayment(db.model):
    __tablename__="quota_repayment"

    id = db.Column(db.Integer(), primary_key=True)
    quota_bill=quota_used=db.Column(db.Integer,db.ForeignKey('quota_bill.id'))
    repayment_amount=db.Column(db.Float())#还款金额
    period=db.Column(db.Integer())#期数
    repayment_date=db.Column(db.Datetime())#日期


