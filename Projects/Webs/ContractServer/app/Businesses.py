#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
#from flask import request
from json.decoder import *
from Projects.Webs.ContractServer.settings import *
from Projects.Webs.ContractServer.app.Functions import *
from Projects.Webs.ContractServer.app.StateCodes import *
from Projects.Webs.ContractServer.database.ContractDatabase import *
from MySqlAlchemy.DBOperator import *
import base64

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
                        if isinstance(json_data, bytes):
                            args = json.loads(str(json_data, encoding='utf-8'))
                        else:
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
    if args is not None:
        user = args.get("username", "")
        pwd = args.get("pwd", "")
        name = args.get("nickname", "未命名")
        company_id = args.get("company_id", -1)
        role_id = args.get("role_id", -1)
        if checkDataVaild(user) and checkDataVaild(pwd):
            exist_objs = records(ContractDB.session(), User, User.user_name == user)
            if len(exist_objs) > 0:
                return buildStandResponse(StateCode_UserExist)
            else:
                pwdmd5 = stringMD5(pwd)  # 加密后的密码
                new_user = User(user_name=user, password=pwdmd5, nick_name=name, company_id=company_id, role_id=role_id)
                addOrRecord(ContractDB.session(), new_user)
                exist_objs = records(ContractDB.session(), User, User.user_name == user)
                if len(exist_objs) > 0:
                    returndata = {}
                    returndata["id"] = exist_objs[0].id
                    returndata["username"] = exist_objs[0].user_name
                    returndata["nickname"] = exist_objs[0].nick_name
                    return buildStandResponse(StateCode_Success, returndata)
                else:
                    return buildStandResponse(StateCode_FailedCreateUser)
        else:
            return buildStandResponse(StateCode_InvaildParam)

#获取角色的授权
def authByRoleID(id):
    auths = []
    if id is not None and id != -1:
        exist_auths = records(ContractDB.session(), RoleAuth, RoleAuth.role_id == id)
        auths = [auth.auth for auth in exist_auths]
    return auths

#获取用户的授权
def authByUserID(id):
    auths = []
    if id is not None and id != -1:
        exist_auths = records(ContractDB.session(), UserAuth, UserAuth.user_id == id)
        auths = [auth.auth for auth in exist_auths]
    return auths

@doResponse
def doUserLogin(request, args=None):
    if args is not None:
        user = args.get("username", "")
        pwd = args.get("pwd", "")
        if checkDataVaild(user) and checkDataVaild(pwd):
            pwdmd5 = stringMD5(pwd)  # 加密后的密码
            exist_users = records(ContractDB.session(), User, and_(User.user_name == user, User.password == pwdmd5))
            if len(exist_users) > 0:
                role_id = exist_users[0].role_id
                returndata = {}
                returndata["id"] = exist_users[0].id
                returndata["username"] = exist_users[0].user_name
                role_data = {}
                role_data["id"] = role_id
                role_data["auths"] = authByRoleID(role_id)
                returndata["role"] = role_data
                returndata["auths"] = authByUserID(exist_users[0].user_name)
                returndata["company_id"] = exist_users[0].company_id
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
            record = records(ContractDB.session(), User, User.id == user)
            if len(record) > 0:
                existuser = record[0]
                if checkDataVaild(authority):
                    existuser.authority_id = authority
                if checkDataVaild(name):
                    existuser.name = name
                addOrRecord(ContractDB.session(), existuser)
                record = records(ContractDB.session(), User, User.id == user)
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
            record = records(ContractDB.session(), Project, Project.name == name)
            if len(record) == 0:
                project = Project(project_name=name)
                addOrRecord(ContractDB.session(), project)
                record = records(ContractDB.session(), Project, Project.name == name)
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
def doContractHistory(request, args=None):
    if args is not None:
        contract_id = args.get("contract_id", "")
        progress = args.get("progress", "")
        pay_money = args.get("pay_money", "")
        #print("-->", name)
        if checkDataVaild(contract_id):
            id = createUuid()
            dt = currentTimeStamp()
            size = addOrRecord(ContractDB.session(), ContractsHistory(id=id, contract_id=contract_id, progress=progress, pay_money=pay_money, datetime = dt))
            if size > 0:
                res = {}
                res["id"] = id
                res["contract_id"] = contract_id
                res["progress"] = progress
                res["pay_money"] = pay_money
                res["datetime"] = dt
                return buildStandResponse(StateCode_Success, res)
            else:
                return buildStandResponse(StateCode_FailedToCreateContractHistory)
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
def getProjectList(request, args=None):
    if args is not None:
        projects = records(ContractDB.session(), Project)
        project_json = {}
        project_json["projects"] = []
        for pro in projects:
            temp = {}
            temp["project_id"] = pro.project_id
            temp["project_name"] = pro.project_name
            project_json["projects"].append(temp)
        return buildStandResponse(StateCode_Success, project_json)

@doResponse
def doCreateRole(request, args=None):
    if args is not None:
        role_name = args.get("name", "")
        if checkDataVaild(role_name):
            objs = records(ContractDB.session(), Role, Role.name == role_name)
            if len(objs) == 0:
                id = createUuid()
                size = addOrRecord(ContractDB.session(), Role(name=role_name))
                if size > 0:
                    res_json = {}
                    res_json["id"] = id
                    res_json["name"] = role_name
                    return buildStandResponse(StateCode_Success, res_json)
                else:
                    return buildStandResponse(StateCode_FailedToCreateRole)
            else:
                return buildStandResponse(StateCode_RoleExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)
@doResponse
def getCompanies(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), Company)
        res_json = {}
        res_json["companies"] = []
        for obj in objects:
            temp = {}
            temp["company_id"] = obj.company_id
            temp["company_name"] = obj.company_name
            res_json["companies"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

@doResponse
def getContractList(request, args=None):
    if args is not None:
        username = args.get("user", "")
        if checkDataVaild(username):
            record = records(ContractDB.session(), User, User.id == username)
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

@doResponse
def doUpload(request, args=None):
    if args is not None:
        filename = args.get("filename", "")
        filedata = args.get("filedata", "")
        classify = args.get("classify", "")
        contract_id = args.get("contract_id", "")
        if checkDataVaild(filename) and checkDataVaild(filedata) and checkDataVaild(contract_id) and checkDataVaild(classify):
            objs = records(ContractDB.session(), Contracts, Contracts.contract_id == contract_id)
            if len(objs) > 0:
                cont = objs[0]
                contName = cont.contract_name
                objs = records(ContractDB.session(), Project, Project.id == cont.project_id)
                if len(objs) > 0:
                    pro = objs[0]
                    proName = pro.project_name
                    dir = os.path.join(FILE_RESTORE_ROOT_DIR,proName, contName, classify)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    fullpath = os.path.join(dir, filename)

                    if os.path.exists(fullpath):
                        return buildStandResponse(StateCode_FileExist)

                    with open(fullpath, "wb", ) as f:
                        print("Write file to:", fullpath)
                        f.write(base64.b64decode(filedata))
                        addOrRecord(ContractDB.session(), File(contract_id=contract_id, path=fullpath))
                    return buildStandResponse(StateCode_Success, {"url":fullpath})
                else:
                    return buildStandResponse(StateCode_ProjectNotExist)
            else:
                return buildStandResponse(StateCode_ContractNotExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doCompanyCreate(request, args=None):
    if args is not None:
        name = args.get("company_name", "")
        #print("-->", name)
        if checkDataVaild(name):
            record = records(ContractDB.session(), Company, Company.name == name)
            if len(record) == 0:
                obj = Company(company_name=name)
                addOrRecord(ContractDB.session(), obj)
                record = records(ContractDB.session(), Company, Company.name == name)
                if len(record) > 0:
                    res = {}
                    res["company_id"] = record[0].company_id
                    res["company_name"] = record[0].company_name
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToCreateCompany)
            else:
                return buildStandResponse(StateCode_CompanyExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)