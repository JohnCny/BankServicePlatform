# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import Service
from .model import Customer
from passlib.apps import custom_app_context as pwd_context

class CustomerService(Service):
    __model__ = Customer

