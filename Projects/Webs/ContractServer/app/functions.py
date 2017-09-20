#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

StateCode_Success = 0
StateCode_UserExist = 1
StateCode_UnsupportMethod = 2
StateCode_InvaildParam = 3
StateCode_FailedCreateUser = 4


StateCodeDescriptions = {StateCode_Success : "成功",
                         StateCode_UserExist : "用户已存在",
                         StateCode_UnsupportMethod : "不支持的方法",
                         StateCode_InvaildParam : "无效的参数",
                         StateCode_FailedCreateUser: "创建用户失败"}

def codeString(code):
    if code in StateCodeDescriptions.keys():
        return StateCodeDescriptions[code]
    else:
        return "未知代码"

def buildStandResponse(code, data = None):
    respone = {}
    #print(code, type(code))
    respone["state"] = code
    respone["message"] = codeString(code)
    respone["data"] = data
    return json.dumps(respone)

def checkStringVaild(str):
    return (str is not None) and (len(str) > 0)

def checkPasswordInvaild(pwd):
    return True