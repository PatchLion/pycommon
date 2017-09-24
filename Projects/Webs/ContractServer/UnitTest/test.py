import unittest
from Projects.Webs.ContractServer.UnitTest.TestFunctions import *
from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.StateCodes import *
from MySqlAlchemy.DBOperator import *
from Projects.Webs.ContractServer.settings import *
import shutil, os


#get("/api/companies/list")

class ApiTest(unittest.TestCase):

    def test_init(self):
        removeRecords(ContractDB.session(), User)
        removeRecords(ContractDB.session(), Role)
        removeRecords(ContractDB.session(), Project)
        removeRecords(ContractDB.session(), Contract)
        removeRecords(ContractDB.session(), ContractHistory)
        removeRecords(ContractDB.session(), Company)
        removeRecords(ContractDB.session(), AskApprove)


    # 用户注册
    def test_user_create(self):
        api = "/api/user/register"

        get(api, {"username": "a", "pwd": "b"}, self.assertEquals, [405])
        post(api, {"username": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_UserExist])
        post(api, {"username": "b", "pwd": "b", "name":"b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "b", "name":"b"}, self.assertEquals, [200, StateCode_InvaildParam])

    #角色注册
    def test_create_role(self):
        api = "/api/role/create"

        get(api, {"name": "role_a"}, self.assertEquals, [200, StateCode_Success])
        get(api, {"name": "role_a"}, self.assertEquals, [200, StateCode_RoleExist])
        post(api, {"name": "role_b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "role_b"}, self.assertEquals, [200, StateCode_RoleExist])
        get(api, {}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {}, self.assertEquals, [200, StateCode_InvaildParam])


    #用户登录
    def test_user_login(self):
        api = "/api/user/login"
        get(api, {"username": "a", "pwd": "b"}, self.assertEquals, [405])
        post(api, {"username": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "a", "pwd": "c"}, self.assertEquals, [200, StateCode_FailedToLogin])
        post(api, {"username": "ccc", "pwd": "c"}, self.assertEquals, [200, StateCode_FailedToLogin])

    #创建项目
    def test_project_create(self):
        api = '/api/project/create'
        get(api, {"name": "三峡大坝", "money": 100000000, "last_date": 10021301203}, self.assertEquals,[405])
        post(api, {"name": "三峡大坝", "money": 100000000, "last_date": 10021301203}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "三峡大坝", "money": 87766, "last_date": 43424}, self.assertEquals, [200, StateCode_ProjectExist])

    #获取项目列表
    def test_project_list(self):
        api = '/api/project/list'
        post(api, {}, self.assertEquals, [405])
        get(api, {}, self.assertEquals, [200, StateCode_Success])

    #创建合同
    def test_contract_create(self):
        api = '/api/contract/create'

        get(api, {"name": "三峡大坝合同", "project_id":1, "company_id":1, "second_party_name":"集团公司"}, self.assertEquals, [405])
        post(api, {"name": "三峡大坝合同", "project_id":1, "company_id":1, "second_party_name":"集团公司"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "三峡大坝合同", "project_id": 1, "company_id": 1, "second_party_name": "集团公司"}, self.assertEquals, [200, StateCode_ContractExist])
        post(api, {"name": "三峡大坝合同1", "project_id": 1, "company_id": 1, }, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"name": "三峡大坝合同2", "project_id": 1, "second_party_name": "集团公司"}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"project_id": 1, "second_party_name": "集团公司"}, self.assertEquals, [200, StateCode_InvaildParam])

        post(api, {"name": "三峡大坝合同3", "project_id":2, "company_id":1, "second_party_name":"财务公司"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "三峡大坝合同4", "project_id":2, "company_id":1, "second_party_name":"人力公司"}, self.assertEquals, [200, StateCode_Success])

    #获取合同
    def test_contract_list(self):
        api = '/api/contract/list'

        get(api, {"project_id":1}, self.assertEquals, [405])
        post(api, {"project_id":1}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id":2, "company_id":1}, self.assertEquals, [200, StateCode_Success])

    # 增加合同执行记录
    def test_contract_history(self):
        api = '/api/contract/history/create'

        get(api, {"contract_id": 1,"progress": 0,"pay_money": 1000}, self.assertEquals, [405])
        post(api, {"contract_id": 1, "progress": 0, "pay_money": 1000}, self.assertEquals, [200, StateCode_Success])
        post(api, {"contract_id": -1, "progress": 0, "pay_money": 1000}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"contract_id": 1, "progress": -1, "pay_money": 1000}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"contract_id": 1, "progress": 0, "pay_money": -1}, self.assertEquals, [200, StateCode_InvaildParam])

    #获取公司列表
    def test_companies_list(self):
        api = '/api/companies/list'


        post(api, {}, self.assertEquals, [405])
        get(api, {}, self.assertEquals, [200, StateCode_Success])

    #创建公司
    def test_companies_list(self):
        api = '/api/companies/create'

        get(api, {"name": "公司1"}, self.assertEquals, [405])
        post(api, {"name": "公司1"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "公司1"}, self.assertEquals, [200, StateCode_CompanyExist])
        post(api, {"name": "公司2"}, self.assertEquals, [200, StateCode_Success])

    # 上传合同附件
    def test_contract_upload(self):
        api = '/api/contract/upload'
        path = os.path.split(os.path.realpath(__file__))[0] + "/../" + FILE_RESTORE_ROOT_DIR
        if os.path.exists(path):
            shutil.rmtree(path)

        get(api, {"filename": "test.txt", "filedata": "1111=", "classify": "测试", "contract_id": 1}, self.assertEquals, [405])
        post(api, {"filename": "test.txt", "filedata": "1111=", "classify": "测试", "contract_id": 1}, self.assertEquals, [200, StateCode_Success])
        post(api, {"filename": "test.txt", "filedata": "1111=", "classify": "测试", "contract_id": 1}, self.assertEquals, [200, StateCode_FileExist])


    # 创建审批请求
    def test_ask_approve_create(self):
        api = '/api/project/ask_approve/create'

        get(api, {"project_id": 0,"first_approve_user_id": 1,"second_approve_user_id": 2}, self.assertEquals, [405])
        post(api, {"project_id": 0, "first_approve_user_id": 3, "second_approve_user_id": 2}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 0, "first_approve_user_id": 3, "second_approve_user_id": 2}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 2, "first_approve_user_id": 1, "second_approve_user_id": 3}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 1, "first_approve_user_id": 1, "second_approve_user_id": 3}, self.assertEquals, [200, StateCode_Success])

    # 获取审批请求
    def test_ask_approve_get(self):
        api = '/api/project/ask_approve/get'

        get(api, {"user_id": 1}, self.assertEquals, [405])
        post(api, {"user_id": 1}, self.assertEquals, [200, StateCode_Success])