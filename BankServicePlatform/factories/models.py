# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from ..tools.helper import JsonSerializer



class BasicModel():
    is_none=0
    def isNone(self):
        return False

class ModelFactory():
    @staticmethod
    def new(query_result,model):
        if query_result is not None:
            return query_result
        else:
            return model.newNone()