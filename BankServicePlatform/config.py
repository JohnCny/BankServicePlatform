# -*- coding: utf-8 -*-
__author__ = 'Johnny'

import sys
import os
import logging
import logging.config

reload(sys)
sys.setdefaultencoding('utf8')

DEBUG = True

SECRET_KEY = '\x9c\n)\xec7 ?o@\x86\xc4\xe5_\x00\x10\xd9A$\xd3\x81\xcd\x1d\xb3\x90'

SQLALCHEMY_DATABASE_URI = 'mysql://root:Qk#13w79@139.196.31.230:3306/bank_service_platform'

SQLALCHEMY_TRACK_MODIFICATIONS=False

PAD_SERVER_URL='139.196.31.230'

REDIS_URL='redis://:Qk$13w79@139.196.31.230:6379/0'

# CELERY_BROKER_URL = 'redis://192.168.3.252:6379/0'

"""
MAIL_DEFAULT_SENDER = 'info@bankserviceplatform.com'
MAIL_SERVER = 'smtp.postmarkapp.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
"""

_HERE = os.path.dirname(__file__)
_DB_SQLITE_PATH = os.path.join(_HERE, 'scapp.sqlite')

# ========配置日志开始=================
_LOG_PATH=os.path.join(_HERE, 'log')
if not os.path.exists(_LOG_PATH):
    os.mkdir(_LOG_PATH)
_LOG_FILE_PATH=os.path.join(_LOG_PATH,'bsp.log')
logger = logging.getLogger('bsp')
hdlr = logging.FileHandler(_LOG_FILE_PATH)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)
