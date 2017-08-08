# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask import Blueprint, render_template

from . import route



bp = Blueprint('/', __name__)


@route(bp, '/')
def index():
    return render_template('login.html')

@route(bp,'/customer')
def customer():
    return render_template('customer.html')



