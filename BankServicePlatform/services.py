# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from .customer.service import CustomerService
from .product.service import ProductService
from .quota.service import QuotaService,QuotaBillService,QuotaRecordService,QuotaRepaymentService,QuotaUsedRecordService

customer=CustomerService()

product=ProductService()

quota=QuotaService()

quota_bill=QuotaBillService()

quota_record=QuotaRecordService()

quota_repayment=QuotaRepaymentService()

quota_used_record=QuotaUsedRecordService()