 # -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import Service
from .model import Quota,QuotaRecord,QuotaBill,QuotaRepayment,QuotaUsedRecord

class QuotaService(Service):
    __model__ = Quota

class QuotaRecordService(Service):
    __model__ = QuotaRecord

class QuotaBillService(Service):
    __model__ = QuotaBill

class QuotaUsedRecordService(Service):
    __model__ = QuotaUsedRecord

class QuotaRepaymentService(Service):
    __model__ = QuotaRepayment