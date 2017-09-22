import unittest
from Projects.Webs.ContractServer.UnitTest.TestFunctions import *
from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.StateCodes import *
from MySqlAlchemy.DBOperator import *

#get("/api/companies/list")

class ApiTest(unittest.TestCase):

    def test_init(self):
        removeRecords(ContractDB.session(), User)
        removeRecords(ContractDB.session(), Roles)

    # 用户注册
    def test_user_create(self):
        api = "/api/user/register"

        get(api, {"user": "a", "pwd": "b"}, self.assertEquals, [405])
        post(api, {"user": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"user": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_UserExist])
        post(api, {"user": "b", "pwd": "b", "name":"b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"user": "b", "name":"b"}, self.assertEquals, [200, StateCode_InvaildParam])

    #角色注册
    def test_create_role(self):
        api = "/api/role/create"

        get(api, {"role_name": "role_a"}, self.assertEquals, [200, StateCode_Success])
        get(api, {"role_name": "role_a"}, self.assertEquals, [200, StateCode_RoleExist])
        post(api, {"role_name": "role_b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"role_name": "role_b"}, self.assertEquals, [200, StateCode_RoleExist])
        get(api, {}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {}, self.assertEquals, [200, StateCode_InvaildParam])

    #用户登录
    def test_user_login(self):
        api = "/api/user/login"
        post(api, {"user": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_Success])