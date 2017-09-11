# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import db
from passlib.apps import custom_app_context as pwd_context
from ..tools.helper import JsonSerializer
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from BankServicePlatform.config import SECRET_KEY
from ..factories.models import BasicModel
from ..factories.gof import Singleton

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))

class CustomerJsonSerializer(JsonSerializer):
    __json_public__ = ["id","real_name","identification_number","phone",'bank_card_number','is_none']

class Customer(CustomerJsonSerializer,db.Model,BasicModel):
    __tablename__="customer"

    id = db.Column(db.Integer(), primary_key=True)

    password=db.Column(db.String(64))
    real_name=db.Column(db.String(8))#姓名
    identification_number=db.Column(db.String(20))#身份证
    phone=db.Column(db.String(20))#手机号码
    channel=db.Column(db.Integer())#渠道
    bank_card_number=db.Column(db.String(25),default=0)#银行卡号
    #flask-security use，未使用flask-security
    email=db.Column(db.String(64))
    active=db.Column(db.Boolean())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    create_date=db.Column(db.DateTime(),default=datetime.datetime.now)#创建时间

    quotaes=db.relationship('Quota', backref='customer',uselist=False)#额度关联

    def is_active(self):
        return self.active

    #密码加密
    def hash_password(self,password):
        self.password=pwd_context.encrypt(password)

    def verify_password(self,password):
        return pwd_context.verify(password,self.password)

    #创建token
    def generate_auth_token(self,expiration=60*60*24):
        s=Serializer(SECRET_KEY,expires_in=expiration)
        return s.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s=Serializer(SECRET_KEY)
        try:
            data=s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        customer=Customer.query.get(data['id'])
        return customer

    #flask-login 使用
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def newNone():
        return NoneCustomer()

class NoneCustomer(Customer,Singleton):
    is_none=1
    def isNone(self):
        return True

