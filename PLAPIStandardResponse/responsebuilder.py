#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class ApiResponseBuilder(object):
    errorStringFunc = None

    @classmethod
    def build(cls, code, msg=None, data=None):
        response = {}
        response["code"] = code
        if msg is None:
            if cls.errorStringFunc is not None:
                response["msg"] = cls.errorStringFunc(code)
            else:
                response["msg"] = ""
        else:
            response["msg"] = msg
        response["data"] = data

        return json.dumps(response, ensure_ascii=False)