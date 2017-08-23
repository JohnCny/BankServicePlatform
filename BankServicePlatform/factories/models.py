# -*- coding: utf-8 -*-
__author__ = 'Johnny'


class BasicModel():

    def isNone(self):
        return False



class ModelFactory():

    def new(self,model):
        if isinstance(model,BasicModel) and model is not None:
            return model
        else:
            return model.newNone()