#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from .StateCodes import *
import hashlib
import uuid
import time

#构建标准响应结果
def buildStandResponse(code, data = None):
    respone = {}
    #print(code, type(code))
    respone["state"] = code
    respone["message"] = codeString(code)
    respone["data"] = data
    return json.dumps(respone,ensure_ascii=False)

#简单检测数据有效性
def checkDataVaild(str):
    return (str is not None) and (len(str) > 0)

#获取字符串MD5值
def stringMD5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    pwdmd5 = md5.hexdigest()
    return pwdmd5

#创建Uuid
def createUuid():
    uid = uuid.uuid4()
    return uid.hex

#创建当前时间戳
def currentTimeStamp():
    return int(time.time())

#将日期转为秒数
def seconds(sec, min, hour, day):
    daysec = day * 24 * 60 * 60
    hoursec = hour * 60 * 60
    minsec = min * 60
    return daysec + hoursec + minsec + sec
