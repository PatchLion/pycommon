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
def doUserModify(request, args=None):
    if args is not None:
        user = args.get("user", "")
        authority = args.get("authority", "")
        name = args.get("name", "")
        if checkDataVaild(user) and (checkDataVaild(authority) or checkDataVaild(name)):
            record = records(ContractDB.session(), User, User.user_id == user)
            if len(record) > 0:
                existuser = record[0]
                if checkDataVaild(authority):
                    existuser.authority_id = authority
                if checkDataVaild(name):
                    existuser.name = name
                addOrRecord(ContractDB.session(), existuser)
                record = records(ContractDB.session(), User, User.user_id == user)
                res = {}
                res["user"] = user
                res["authority"] = record[0].authority_id
                res["name"] = record[0].name
                return buildStandResponse(StateCode_Success, res)
            else:
                return buildStandResponse(StateCode_UserNotExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doProjectCreate(request, args=None):
    if args is not None:
        name = args.get("project_name", "")
        #print("-->", name)
        if checkDataVaild(name):
            record = records(ContractDB.session(), Projects, Projects.project_name == name)
            if len(record) == 0:
                project = Projects(project_name=name)
                addOrRecord(ContractDB.session(), project)
                record = records(ContractDB.session(), Projects, Projects.project_name == name)
                if len(record) > 0:
                    res = {}
                    res["project_id"] = record[0].project_id
                    res["project_name"] = record[0].project_name
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToCreateProject)
            else:
                return buildStandResponse(StateCode_ProjectExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doContractCreate(request, args=None):
    if args is not None:
        project_id= args.get("project_id", "")
        contract_name= args.get("contract_name", "")
        company_id= args.get("company_id", "")
        retention_money= args.get("retention_money", "")
        retention_money_date= args.get("retention_money_date", "")
        parent_contract_id= args.get("parent_contract_id", "")
        money= args.get("money", "")
        #print("-->", name)
        if checkDataVaild(contract_name):
            record = records(ContractDB.session(), Contracts, Contracts.contract_name == contract_name)
            if len(record) == 0:
                contract = Contracts(contract_id=createUuid(), project_id=project_id,contract_name=contract_name, company_id=company_id, retention_money= retention_money, retention_money_date=retention_money_date, parent_contract_id=parent_contract_id, money=money)
                addOrRecord(ContractDB.session(), contract)
                record = records(ContractDB.session(), Contracts, Contracts.contract_name == contract_name)
                if len(record) > 0:
                    res = {}
                    res["contract_id"] = record[0].contract_id
                    res["project_id"] = record[0].project_id
                    res["contract_name"] = record[0].contract_name
                    res["company_id"] = record[0].company_id
                    res["retention_money"] = record[0].retention_money
                    res["retention_money_date"] = record[0].retention_money_date
                    res["parent_contract_id"] = record[0].parent_contract_id
                    res["money"] = record[0].money
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToCreateProject)
            else:
                return buildStandResponse(StateCode_ContractExist)
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

@doResponse
def getProjectList(request, args=None):
    if args is not None:
        projects = records(ContractDB.session(), Projects)
        project_json = {}
        project_json["projects"] = []
        for pro in projects:
            temp = {}
            temp["project_id"] = pro.project_id
            temp["project_name"] = pro.project_name
            project_json["projects"].append(temp)
        return buildStandResponse(StateCode_Success, project_json)

@doResponse
def getContractList(request, args=None):
    if args is not None:
        username = args.get("user", "")
        if checkDataVaild(username):
            record = records(ContractDB.session(), User, User.user_id == username)
            if len(record) == 0:
                return buildStandResponse(StateCode_UserNotExist)

            user = record[0]

            contracts = records(ContractDB.session(), Contracts)

            res_json = {}
            res_json["contracts"] = []
            for cont in contracts:
                if cont.company_id == user.company_id or -1 == user.company_id:
                    res = {}
                    res["contract_id"] = cont.contract_id
                    res["project_id"] = cont.project_id
                    res["contract_name"] = cont.contract_name
                    res["company_id"] = cont.company_id
                    res["retention_money"] = cont.retention_money
                    res["retention_money_date"] = cont.retention_money_date
                    res["parent_contract_id"] = cont.parent_contract_id
                    res["money"] = cont.money
                    res_json["contracts"].append(res)
            return buildStandResponse(StateCode_Success, res_json)
        else:
            return buildStandResponse(StateCode_InvaildParam)