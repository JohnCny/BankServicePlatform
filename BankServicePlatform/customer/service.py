# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import Service
from .model import Customer
from passlib.apps import custom_app_context as pwd_context

class CustomerService(Service):
    __model__ = Customer

    def _preprocess_params(self, kwargs):
        kwargs=super(CustomerService,self)._preprocess_params(kwargs)
        return kwargs.get('customer')
