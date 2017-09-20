from flask import request
from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app import app
from Projects.Webs.ContractServer.app.functions import *
from MySqlAlchemy.DBOperator import *
import hashlib
md5 = hashlib.md5()

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to ContractServer!"

#注册用户
@app.route('/regist', methods=["POST", "GET"])
def regist():
    if "GET" == request.method:
        user = request.args.get("user", "")
        pwd = request.args.get("pwd", "")
        name = request.args.get("name", "")
        if checkStringVaild(user) and checkStringVaild(pwd):
            record = records(ContractDB.session(), User, User.user_id == user)
            if len(record) > 0:
                return buildStandResponse(StateCode_UserExist)
            else:
                md5.update(pwd.encode('utf-8'))
                pwd = md5.hexdigest() #加密后的密码
                if not checkStringVaild(name):
                    name = "未命名"
                new_user = User(user_id=user, password=pwd, name=name)
                addOrRecord(ContractDB.session(), new_user)
                record = records(ContractDB.session(), User, User.user_id == user)

                if len(record) > 0:
                    return buildStandResponse(StateCode_Success)
                else:
                    return buildStandResponse(StateCode_FailedCreateUser)
        else:
            return buildStandResponse(StateCode_InvaildParam)

    elif "POST" == request.method:
        return buildStandResponse(StateCode_UnsupportMethod)