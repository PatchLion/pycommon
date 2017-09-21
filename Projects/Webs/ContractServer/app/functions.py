#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from .StateCodes import *
import hashlib
import uuid
import time


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
    return json.dumps(respone,ensure_ascii=False)

def checkDataVaild(str):
    return (str is not None) and (len(str) > 0)




def stringMD5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    pwdmd5 = md5.hexdigest()
    return pwdmd5


def createUuid():
    uid = uuid.uuid4()
    return uid.hex

def currentTimeStamp():
    return int(time.time())

def seconds(sec, min, hour, day):
    daysec = day * 24 * 60 * 60
    hoursec = hour * 60 * 60
    minsec = min * 60
    return daysec + hoursec + minsec + sec