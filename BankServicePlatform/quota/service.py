 # -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..core import Service
from .model import Quota

class QuotaService(Service):
    __model__ = Quota