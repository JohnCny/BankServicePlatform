# -*- coding: utf-8 -*-
__author__ = 'Johnny'

import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding('utf8')

# 初始化
app = Flask(__name__)

# 读取配置文件
app.config.from_object('BankServicePlatform.settings.ProConfig') # mysql

# 初始化数据库
db = SQLAlchemy(app)