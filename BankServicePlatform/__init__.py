# -*- coding: utf-8 -*-
__author__ = 'Johnny'

import sys
from tools import helper
from flask import Flask
from .core import db

reload(sys)
sys.setdefaultencoding('utf8')

# 初始化
app = Flask(__name__)

# 读取配置文件
app.config.from_object('BankServicePlatform.settings.ProConfig') # mysql






