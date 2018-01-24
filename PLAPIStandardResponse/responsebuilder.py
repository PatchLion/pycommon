#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from enum import Enum

class ApiResponseBuilder(object):
    errorStringFunc = None

    @classmethod
    def build(cls, code, msgExt=None, data=None):
        response = {}
        if isinstance(code, Enum):
            response["code"] = code.value
        else:
            response["code"] = code


        if cls.errorStringFunc is not None:
            response["msg"] = cls.errorStringFunc(code)
        else:
            response["msg"] = "未知状态"

        if msgExt is not None:
            response["msg"] = response["msg"] + ("%s" % msgExt)

        response["data"] = data

        return json.dumps(response, ensure_ascii=False)

