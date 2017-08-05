# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from BankServicePlatform import db


class Quota(db.Model):
    __tablename__="quota"

    id = db.Column(db.Integer(), primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'))
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'))
    amount=db.Column(db.Integer())#总额度
    available_amount=db.Column(db.Float())#可用额度
    version=db.Column(db.Integer())#防并发，每次更新该值+1

    quota_recordes=db.relationship('QuotaRecord', backref='quota',lazy='dynamic')#额度记录
    quota_user_recordes=db.relationship('QuotaUsedRecord', backref='quota',lazy='dynamic')#使用额度记录

class QuotaRecord(db.Model):
    __tablename__="quota_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota_id=db.Column(db.Integer,db.ForeignKey('quota.id'))
    create_date=db.Column(db.DateTime())#日期
    original_quota=db.Column(db.Integer())#原始额度
    updated_quota=db.Column(db.Integer())#变更后额度

class QuotaUsedRecord(db.Model):
    __tablename__="quota_used_record"

    id = db.Column(db.Integer(), primary_key=True)
    quota_id=db.Column(db.Integer,db.ForeignKey('quota.id'))
    used_quota=db.Column(db.Integer())#使用额度
    create_date=db.Column(db.DateTime())#日期
    status=db.Column(db.Integer())#当前状态

    quota_billes=db.relationship('QuotaBill', backref='quota_used_record',uselist=False)#额度账单

class QuotaBill(db.Model):
    __tablename__="quota_bill"

    id = db.Column(db.Integer(), primary_key=True)
    quota_used_record_id=db.Column(db.Integer,db.ForeignKey('quota_used_record.id'))
    period_amount=db.Column(db.Float())#每期还款金额
    period_remain=db.Column(db.Integer())#剩余期数
    create_date=db.Column(db.DateTime())#日期

    quota_repaymentes=db.relationship('QuotaRepayment', backref='quota_bill',lazy='dynamic')#账单还款记录

class QuotaRepayment(db.Model):
    __tablename__="quota_repayment"

    id = db.Column(db.Integer(), primary_key=True)
    quota_bill_id=db.Column(db.Integer,db.ForeignKey('quota_bill.id'))
    repayment_amount=db.Column(db.Float())#还款金额
    period=db.Column(db.Integer())#期数
    repayment_date=db.Column(db.DateTime())#日期


