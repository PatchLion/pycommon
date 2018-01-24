#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import *
from pycommon.PLDatabase import DBInstance
from pycommon.PLLogger import buildLogger
from pycommon.PLArgsChecker import ArgsChecker
from pycommon.PLAPIStandardResponse import flaskResponse
from pycommon.PLAPIStandardResponse import ApiResponseBuilder
from .tables import *
import time, logging

app = Flask(__name__)
keys = []

def runStatisticsApp(host="0.0.0.0", debug=True,  port=13000):
    global keys
    buildLogger(app.logger, level=logging.DEBUG)
    keys = [r.keyvalue for r in DBInstance.records(StatisticsKeys)]
    app.run(host=host, debug=debug, port=port)

@app.route("/statistics/view", methods=["GET"])
def viewStatistics():
    return doViewStatistics(request, None)

@flaskResponse
def doViewStatistics(request, args):
    if args is not None:
        checker = ArgsChecker(args)
        key = checker.addStringChecker("key", is_req=True)# 页面路径
        page = checker.addStringChecker("page", is_req=True)# 页面路径
        title = checker.addStringChecker("title", is_req=True)# 页面标题
        appversion = checker.addStringChecker("appversion", is_req=True)# app版本
        clientid = checker.addStringChecker("clientid", is_req=True)# 客户端id

        successed, message = checker.checkResult()

        if not successed:
            return ApiResponseBuilder.build(code=-1, msgExt=message)

        global keys
        if key not in keys:
            return ApiResponseBuilder.build(code=-1, msgExt="无效的授权key")

        vs = ViewStatistics( page=page, title=title, appversion=appversion, clientid=clientid, datetime=time.time())

        size = DBInstance.addRecord(vs)
        if size > 0:
            return ApiResponseBuilder.build(code=0)
        else:
            return ApiResponseBuilder.build(code=-1, msgExt="添加页面统计失败")


@app.route("/statistics/event", methods=["GET"])
def eventStatistics():
    return doEventStatistics(request, None)

@flaskResponse
def doEventStatistics(request, args):
    if args is not None:
        checker = ArgsChecker(args)
        key = checker.addStringChecker("key", is_req=True)# 页面路径
        action = checker.addStringChecker("action", is_req=True)# 页面路径
        label = checker.addStringChecker("label", is_req=True)# 页面标题
        appversion = checker.addStringChecker("appversion", is_req=True)# app版本
        clientid = checker.addStringChecker("clientid", is_req=True)# 客户端id

        successed, message = checker.checkResult()

        if not successed:
            return ApiResponseBuilder.build(code=-1, msgExt=message)

        global keys
        if key not in keys:
            return ApiResponseBuilder.build(code=-1, msgExt="无效的授权key")

        es = EventStatistics(action=action, label=label, appversion=appversion, clientid=clientid, datetime=time.time())

        size = DBInstance.addRecord(es)
        if size > 0:
            return ApiResponseBuilder.build(code=0)
        else:
            return ApiResponseBuilder.build(code=-1, msgExt="添加时间统计失败")