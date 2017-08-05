# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import Service
from .model import Customer

class CustomerService(Service):
    __model__ = Customer