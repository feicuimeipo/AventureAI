# -*- coding: utf-8 -*-
from common.utilities.JsonUtils import class_to_json


class ResponseDTO:
    code = 0
    message = ""
    data = None

    def ok(self):
        self.code = 0
        self.message ="操作成功"
        return self

    def setData(self,data):
        self.data = data
        return self

    def error(self, message):
        self.code = 500
        self.message = message
        return self

    def setCode(self, code):
        self.code = code
        return self

    def getCode(self):
        return self.code

    def setMessage(self,message):
        self.message = message
        return self

    def setErrorCode(self,code,message):
        self.code = code
        self.message = message
        return self

    def toJson(self):
        return class_to_json(self)