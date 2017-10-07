from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.Functions import stringMD5, createUuid
from MySqlAlchemy.DBOperator import *


ContractDB.initTables()

#增加角色表
removeRecords(ContractDB.session(), Role)
admin_role_id = createUuid()
test_role1_id = createUuid()
test_role2_id = createUuid()
addOrRecord(ContractDB.session(), Role(name ="管理员")) #管理员权限
addOrRecord(ContractDB.session(), Role(name ="测试角色1")) #
addOrRecord(ContractDB.session(), Role(name ="测试角色2")) #

#增加用户
removeRecords(ContractDB.session(), User)
#addOrRecord(ContractDB.session(), User(user_name="root", password=stringMD5("root"), nick_name="root"))
addOrRecord(ContractDB.session(), User(user_name="admin", password=stringMD5("admin"), nick_name="Adminstrator"))
addOrRecord(ContractDB.session(), User(user_name="simpleLove", password=stringMD5("simpleLove"), nick_name="SimpleLove"))
addOrRecord(ContractDB.session(), User(user_name="patchlion", password=stringMD5("patchlion"), nick_name="打补丁的狮子"))

#增加项目
removeRecords(ContractDB.session(), Project)
addOrRecord(ContractDB.session(), Project(name="成都市政项目", addr="11231", trade_id=1, buildtype_id = 1, content= "test", start_date= currentTimeStamp(), last_date=currentTimeStamp()+100000))
addOrRecord(ContractDB.session(), Project(name="三峡大坝项目", addr="11231", trade_id=1, buildtype_id = 1, content= "12312312", start_date= currentTimeStamp(), last_date=currentTimeStamp()+100000))

#增加公司
removeRecords(ContractDB.session(), Company)
addOrRecord(ContractDB.session(), Company(name="设计一公司"))
addOrRecord(ContractDB.session(), Company(name="建设一公司"))
addOrRecord(ContractDB.session(), Company(name="外包一公司", is_outsourced=True))

#增加合同
removeRecords(ContractDB.session(), Contract)
'''
addOrRecord(ContractDB.session(), Contract(name="合同1", project_id=1, company_id=1, money=100000, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同2", project_id=1, company_id=1, money=100000, parent_contract_id=1, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同3", project_id=1, company_id=1, money=100000, parent_contract_id=2, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同4", project_id=1, company_id=1, money=100000, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同5", project_id=1, company_id=1, money=100000, parent_contract_id=4, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同6", project_id=1, company_id=1, money=100000, parent_contract_id=5, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同7", project_id=1, company_id=3, money=100000, parent_contract_id=5, second_party_name="啦啦啦啦啊"))
'''

#增加行业
removeRecords(ContractDB.session(), Trade)

addOrRecord(ContractDB.session(), Trade(name="建筑"))
addOrRecord(ContractDB.session(), Trade(name="保险业"))
addOrRecord(ContractDB.session(), Trade(name="采矿"))
addOrRecord(ContractDB.session(), Trade(name="能源"))
addOrRecord(ContractDB.session(), Trade(name="机械制造"))
addOrRecord(ContractDB.session(), Trade(name="电讯业"))
addOrRecord(ContractDB.session(), Trade(name="房地产"))
addOrRecord(ContractDB.session(), Trade(name="公益组织"))
addOrRecord(ContractDB.session(), Trade(name="广告业"))
addOrRecord(ContractDB.session(), Trade(name="航空航天"))
addOrRecord(ContractDB.session(), Trade(name="计算机"))
addOrRecord(ContractDB.session(), Trade(name="金属冶炼"))
addOrRecord(ContractDB.session(), Trade(name="警察"))
addOrRecord(ContractDB.session(), Trade(name="消防"))
addOrRecord(ContractDB.session(), Trade(name="会计"))
addOrRecord(ContractDB.session(), Trade(name="运输业"))

#增加建设类型
removeRecords(ContractDB.session(), BuildType)

addOrRecord(ContractDB.session(), BuildType(name="改建"))
addOrRecord(ContractDB.session(), BuildType(name="建设"))

#增加资金来源类型
removeRecords(ContractDB.session(), MoneyType)

addOrRecord(ContractDB.session(), MoneyType(name="自筹"))
addOrRecord(ContractDB.session(), MoneyType(name="贷款"))
addOrRecord(ContractDB.session(), MoneyType(name="上级拨付"))
