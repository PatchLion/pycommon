#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class StandResponseBuilder(object):
    #标准json数据返回格式
    @classmethod
    def build(cls, message="", data = None):
        response = {}
        response["msg"] = message #message为空, 代表成功
        response["data"] = data
        return json.dumps(response, ensure_ascii=False)

if "__main__" == __name__:
    print(StandResponseBuilder.build())
    print(StandResponseBuilder.build())
    print(StandResponseBuilder.build("错误代码1"))
    print(StandResponseBuilder.build("错误代码2"))