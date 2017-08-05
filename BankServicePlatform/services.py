# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from .customer.service import CustomerService
from .product.service import ProductService
from .quota.service import QuotaService

customer=CustomerService()

product=ProductService()

quota=QuotaService()