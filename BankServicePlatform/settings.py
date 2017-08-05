# coding:utf-8
__author__ = 'Johnny'

import os

# 引入日志模块
import logging
import logging.config

_HERE = os.path.dirname(__file__)

"""========配置日志开始================="""
_LOG_PATH = os.path.join(_HERE, 'log')
if not os.path.exists(_LOG_PATH):
    os.mkdir(_LOG_PATH)
_LOG_FILE_PATH = os.path.join(_LOG_PATH, 'bsp.log')
logger = logging.getLogger('bsp')
hdlr = logging.FileHandler(_LOG_FILE_PATH)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)
"""===================================="""

"""========配置数据库开始================="""
#本地
_DBUSER = "root"  # 数据库用户名
_DBPASS = "root"  # 数据库用户名密码
_DBHOST = "192.168.3.252"  # 服务器
_DBPORT = '3306'  #服务器端口
_DBNAME = "bsp"  # 数据库名称
#远程
# _DBUSER = "root"  # 数据库用户名
# _DBPASS = "Qkroot"  # 数据库用户名密码
# _DBHOST = "localhost"  # 服务器
# _DBPORT = '3306' #服务器端口
# _DBNAME = "new_oa"  # 数据库名称
"""========配置数据库结束================="""


PER_PAGE = 10  # 每页数量
UPLOAD_FOLDER_REL = '/frontend/static/upload'  #上传目录(相对路径)
UPLOAD_FOLDER_ABS = os.path.join(_HERE, '/frontend/static/upload')  #上传目录(绝对路径)


class Config(object):
    SECRET_KEY = '\x9c\n)\xec7 ?o@\x86\xc4\xe5_\x00\x10\xd9A$\xd3\x81\xcd\x1d\xb3\x90'
    DEBUG = False
    TESTING = False
    BABEL_DEFAULT_TIMEZONE = 'Asia/Chongqing'


class ProConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBPORT, _DBNAME)
    DEBUG = True

class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
