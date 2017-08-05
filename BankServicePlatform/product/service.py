# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import Service
from .model import Product

class ProductService(Service):
    __model__ = Product