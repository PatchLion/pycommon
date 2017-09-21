#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import request
from json.decoder import *
from Projects.Webs.ContractServer.app.Functions import *
from Projects.Webs.ContractServer.app.StateCodes import *
from Projects.Webs.ContractServer.database.ContractDatabase import *
from MySqlAlchemy.DBOperator import *

#args不为None时，证明已经通过参数验证, 外部调用请勿传args

def doResponse(func):
    def wrapper(request,args):
        supports_methods = ["POST", "GET"]
        print(request.method)
        if request.method in supports_methods:
            args = {}
            if "POST" == request.method:
                json_data = request.get_data()
                print("POST json data:", json_data)
                if checkDataVaild(json_data):
                    try:
                        args = json.loads(json_data)
                    except JSONDecodeError as e:
                        return buildStandResponse(StateCode_InvaildDataFormat)
            elif "GET" == request.method:
                args = request.args
            print("GET args:", args)
            return func(None, args)
        else:
            return buildStandResponse(StateCode_UnsupportMethod)
    return wrapper


@doResponse
def doRegister(request, args=None):
    print("1")
    if args is not None:
        user = args.get("user", "")
        pwd = args.get("pwd", "")
        name = args.get("name", "")
        if checkDataVaild(user) and checkDataVaild(pwd):
            record = records(ContractDB.session(), User, User.user_id == user)
            if len(record) > 0:
                return buildStandResponse(StateCode_UserExist)
            else:
                pwdmd5 = stringMD5(pwd)  # 加密后的密码
                if not checkDataVaild(name):
                    name = "未命名"
                new_user = User(user_id=user, password=pwdmd5, name=name)
                addOrRecord(ContractDB.session(), new_user)
                record = records(ContractDB.session(), User, User.user_id == user)

                if len(record) > 0:
                    returndata = {}
                    returndata["user"] = user
                    returndata["name"] = name
                    returndata["authority"] = record[0].authority_id
                    returndata["company"] = record[0].company_id
                    return buildStandResponse(StateCode_Success, returndata)
                else:
                    return buildStandResponse(StateCode_FailedCreateUser)
        else:
            return buildStandResponse(StateCode_InvaildParam)


@doResponse
def doUserLogin(request, args=None):
    if args is not None:
        user = args.get("user", "")
        pwd = args.get("pwd", "")
        if checkDataVaild(user) and checkDataVaild(pwd):
            pwdmd5 = stringMD5(pwd)  # 加密后的密码
            print(pwd, "--->", pwdmd5)
            record = records(ContractDB.session(), User, and_(User.user_id == user, User.password == pwdmd5))
            if len(record) > 0:
                token = Tokens(user_id=user, token=createUuid(), timestamp=currentTimeStamp() + seconds(0, 0, 0, 30))
                addOrRecord(ContractDB.session(), token)
                returndata = {}
                returndata["user"] = token.user_id
                returndata["token"] = token.token
                returndata["expiry"] = token.timestamp
                return buildStandResponse(StateCode_Success, returndata)
            else:
                return buildStandResponse(StateCode_FailedToLogin)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def getAuthorityList(request, args=None):
    if args is not None:
        authoritys = records(ContractDB.session(), Authority)
        auth_json = {}
        auth_json["authorities"] = []
        for auth in authoritys:
            temp = {}
            temp["authority"] = auth.authority_id
            temp["name"] = auth.authority_name
            auth_json["authorities"].append(temp)
        return buildStandResponse(StateCode_Success, auth_json)
