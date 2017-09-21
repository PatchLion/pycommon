from flask import request
from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app import app
from Projects.Webs.ContractServer.app.functions import *
from MySqlAlchemy.DBOperator import *
from .StateCodes import *
from json.decoder import *


@app.route('/')
@app.route('/index')
def index():
    return "Welcome to ContractServer!"

#注册用户
@app.route('/api/user/register', methods=["POST"])
def regist():
    if "POST" == request.method:
        json_data = request.get_data()
        print("json_data:", json_data)
        if checkDataVaild(json_data):
            try:
                data = json.loads(json_data)
                user = data.get("user", "")
                pwd = data.get("pwd", "")
                name = data.get("name", "")
                return userRegister(user, pwd, name)
            except JSONDecodeError as e:
                return buildStandResponse(StateCode_InvaildDataFormat)
        else:
            return buildStandResponse(StateCode_InvaildParam)
    else:
        return buildStandResponse(StateCode_UnsupportMethod)

def userRegister(user, pwd, name = ""):
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

# 登录
@app.route('/api/user/login', methods=["POST"])
def login():
    if "POST" == request.method:
        json_data = request.get_data()
        print("json_data:", json_data)
        if checkDataVaild(json_data):
            try:
                data = json.loads(json_data)
                user = data.get("user", "")
                pwd = data.get("pwd", "")
                return userLogin(user, pwd)
            except JSONDecodeError as e:
                return buildStandResponse(StateCode_InvaildDataFormat)
        else:
            return buildStandResponse(StateCode_InvaildParam)
    else:
        return buildStandResponse(StateCode_UnsupportMethod)

def userLogin(user, pwd):
    if checkDataVaild(user) and checkDataVaild(pwd):
        pwdmd5 = stringMD5(pwd)  # 加密后的密码
        print(pwd, "--->", pwdmd5)
        record = records(ContractDB.session(), User, and_(User.user_id == user, User.password == pwdmd5))
        if len(record) > 0:
            token = Tokens(user_id = user, token = createUuid(), timestamp=currentTimeStamp()+seconds(0,0,0,30))
            addOrRecord(ContractDB.session(), token)
            returndata={}
            returndata["user"] = token.user_id
            returndata["token"] = token.token
            returndata["expiry"] = token.timestamp
            return buildStandResponse(StateCode_Success, returndata)
        else:
            return buildStandResponse(StateCode_FailedToLogin)