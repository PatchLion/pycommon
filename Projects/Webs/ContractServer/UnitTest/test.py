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
        pass

    def test_all(self):
        # 角色注册
        api = "/api/role/create"
        removeRecords(ContractDB.session(), Role)
        get(api, {"name": "role_a"}, self.assertEquals, [405])
        post(api, {"name": "role_b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "role_b"}, self.assertEquals, [200, StateCode_RoleExist])
        post(api, {}, self.assertEquals, [200, StateCode_InvaildParam])


        # 角色列表
        api = "/api/role/list"
        get(api, {}, self.assertEquals, [405])
        post(api, {}, self.assertEquals, [200, StateCode_Success])

        # 用户注册
        api = "/api/user/register"
        removeRecords(ContractDB.session(), User)
        get(api, {"username": "a", "pwd": "b"}, self.assertEquals, [405])
        post(api, {"username": "a", "pwd": "b", "role_id":1}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_UserExist])
        post(api, {"username": "b", "pwd": "b", "name":"b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "b", "name":"b"}, self.assertEquals, [200, StateCode_InvaildParam])

        # 用户登录
        api = "/api/user/login"
        get(api, {"username": "a", "pwd": "b"}, self.assertEquals, [405])
        post(api, {"username": "a", "pwd": "b"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "a", "pwd": "c"}, self.assertEquals, [200, StateCode_FailedToLogin])
        post(api, {"username": "ccc", "pwd": "c"}, self.assertEquals, [200, StateCode_FailedToLogin])

        # 修改用户属性
        api = "/api/user/modify"
        get(api, {"username": "a", "nickname": "测试"}, self.assertEquals, [405])
        post(api, {"username": "a", "nickname": "测试", "auths":[1, 3]}, self.assertEquals, [200, StateCode_Success])
        post(api, {"username": "a", "nickname": "测试", "password":{"old":"b", "new":"c"}}, self.assertEquals, [200, StateCode_Success])


        # 用户列表
        api = "/api/user/list"
        get(api, {}, self.assertEquals, [405])
        post(api, {}, self.assertEquals, [200, StateCode_Success])

        #创建项目
        api = '/api/project/create'
        removeRecords(ContractDB.session(), Project)
        get(api, {"name": "三峡大坝", "money": 100000000, "last_date": 10021301203}, self.assertEquals,[405])
        post(api, {"name": "三峡大坝", "money": 100000000, "start_date": 100000000, "last_date": 10021301203}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "三峡大坝", "money": 100000000, "start_date": 100000000, "last_date": 10021301203}, self.assertEquals, [200, StateCode_ProjectExist])

        #获取项目列表
        api = '/api/project/list'
        get(api, {}, self.assertEquals, [405])
        post(api, {}, self.assertEquals, [200, StateCode_Success])
        post(api, {"id":1, "name": "三峡大坝"}, self.assertEquals, [200, StateCode_Success])

        #创建合同
        api = '/api/contract/create'

        removeRecords(ContractDB.session(), Contract)
        get(api, {"name": "三峡大坝合同", "project_id":1, "company_id":1, "second_party_name":"集团公司"}, self.assertEquals, [405])
        post(api, {"name": "三峡大坝合同", "project_id":1, "company_id":1, "second_party_name":"集团公司"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "三峡大坝合同", "project_id": 1, "company_id": 1, "second_party_name": "集团公司"}, self.assertEquals, [200, StateCode_ContractExist])
        post(api, {"name": "三峡大坝合同1", "project_id": 1, "company_id": 1, }, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"name": "三峡大坝合同2", "project_id": 1, "second_party_name": "集团公司"}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"project_id": 1, "second_party_name": "集团公司"}, self.assertEquals, [200, StateCode_InvaildParam])

        post(api, {"name": "三峡大坝合同3", "project_id":2, "company_id":1, "second_party_name":"财务公司"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "三峡大坝合同4", "project_id":2, "company_id":1, "second_party_name":"人力公司"}, self.assertEquals, [200, StateCode_Success])

        # 上传合同附件
        api = '/api/contract/upload'

        removeRecords(ContractDB.session(), File)
        path = os.path.split(os.path.realpath(__file__))[0] + "/../" + FILE_RESTORE_ROOT_DIR
        if os.path.exists(path):
            shutil.rmtree(path)

        get(api, {"filename": "test.txt", "filedata": "1111=", "classify": "测试", "contract_id": 1}, self.assertEquals, [405])
        post(api, {"filename": "test.txt", "filedata": "1111=", "classify": "测试", "contract_id": 1}, self.assertEquals, [200, StateCode_Success])
        post(api, {"filename": "test.txt", "filedata": "1111=", "classify": "测试", "contract_id": 1}, self.assertEquals, [200, StateCode_FileExist])


        #获取合同
        api = '/api/contract/list'

        get(api, {"project_id":1}, self.assertEquals, [405])
        post(api, {"project_id":1}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id":2, "company_id":1}, self.assertEquals, [200, StateCode_Success])

        # 增加合同执行记录
        api = '/api/contract/history/create'

        removeRecords(ContractDB.session(), ContractHistory)
        get(api, {"contract_id": 1,"progress": 0,"pay_money": 1000}, self.assertEquals, [405])
        post(api, {"contract_id": 1, "progress": 0, "pay_money": 1000}, self.assertEquals, [200, StateCode_Success])
        post(api, {"contract_id": -1, "progress": 0, "pay_money": 1000}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"contract_id": 1, "progress": -1, "pay_money": 1000}, self.assertEquals, [200, StateCode_InvaildParam])
        post(api, {"contract_id": 1, "progress": 0, "pay_money": -1}, self.assertEquals, [200, StateCode_InvaildParam])

        #创建公司
        api = '/api/companies/create'

        removeRecords(ContractDB.session(), Company)
        get(api, {"name": "公司1"}, self.assertEquals, [405])
        post(api, {"name": "公司1"}, self.assertEquals, [200, StateCode_Success])
        post(api, {"name": "公司1"}, self.assertEquals, [200, StateCode_CompanyExist])
        post(api, {"name": "公司2"}, self.assertEquals, [200, StateCode_Success])

        # 获取公司列表
        api = '/api/companies/list'

        get(api, {}, self.assertEquals, [405])
        post(api, {}, self.assertEquals, [200, StateCode_Success])

        # 创建审批请求
        api = '/api/project/ask_approve/create'

        removeRecords(ContractDB.session(), AskApprove)
        get(api, {"project_id": 0,"first_approve_user_id": 1,"second_approve_user_id": 2}, self.assertEquals, [405])
        post(api, {"project_id": 0, "first_approve_user_id": 3, "second_approve_user_id": 2}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 0, "first_approve_user_id": 3, "second_approve_user_id": 2}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 2, "first_approve_user_id": 1, "second_approve_user_id": 3}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 1, "first_approve_user_id": 1, "second_approve_user_id": 3}, self.assertEquals, [200, StateCode_Success])

        #设置审批状态
        api = "/api/project/ask_approve/set"

        get(api, {"project_id": 0, "user_id": 3, "state": Approve_Passed}, self.assertEquals, [405])
        post(api, {"project_id": 0, "user_id": 3, "state": Approve_Rejected}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 0, "user_id": 2, "state": Approve_Passed}, self.assertEquals, [200, StateCode_FailedToSetProjectApprove])
        post(api, {"project_id": 0, "user_id": 3, "state": Approve_Passed}, self.assertEquals, [200, StateCode_Success])
        post(api, {"project_id": 0, "user_id": 2, "state": Approve_Passed}, self.assertEquals, [200, StateCode_Success])

        # 获取审批请求
        api = '/api/project/ask_approve/get'

        get(api, {"user_id": 1}, self.assertEquals, [405])
        post(api, {"user_id": 1}, self.assertEquals, [200, StateCode_Success])

